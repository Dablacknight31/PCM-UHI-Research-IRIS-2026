"""Read saved results and verify the protected cooling calculations. No solvers."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

EXPECTED = {'PCM-011': (0.456, 0.697), 'PCM-067': (0.501, 0.797), 'PCM-069': (0.503, 0.819)}

def cooling_extrema(hourly, spatial):
    """Keep hourly area/time means separate from grid-cell/substep extrema.

    hotspot_mean_K already contains the original trapezoidal time integral and
    hotspot area weighting. max_cooling_K tracks the maximum negative cell state
    over both endpoints of every solver substep, before hourly aggregation.
    peak_cool_K is a synchronous spatial snapshot selected at a global minimum.
    """
    mean = hourly['hotspot_mean_K'].to_numpy()
    index = int(np.argmin(mean))
    return {
        'maximum_hourly_hotspot_cooling_K': max(0.0, -float(mean[index])),
        'hour_start_UTC': str(hourly.iloc[index]['datetime_UTC']),
        'maximum_hotspot_cell_substep_cooling_K': float(hourly['hotspot_max_cooling_K'].max()),
        'maximum_domain_grid_cell_cooling_K': max(0.0, -float(np.min(spatial['peak_cool_K']))),
    }

def verify_saved_results(root):
    """Verify saved chronology, matched controls, forcing, extrema and masks."""
    root = Path(root)
    c1 = root / 'results/category1'
    snapshot = root / 'results/category3/accepted_baselines'
    manifest = json.loads((c1 / 'category1_manifest.json').read_text())
    checks = []
    def require(name, condition):
        checks.append({'check': name, 'passed': bool(condition)})
        if not condition:
            raise ValueError(name)
    workbook = root / 'data/inputs/materials/PCM_Details_As_Executed.xlsx'
    require('As-executed workbook hash', hashlib.sha256(workbook.read_bytes()).hexdigest() == '0dda90b01987f99819c24ff1f7b18d51bfee4d3ea73358f73c7e616977e76aed')
    extrema = []
    for folder in sorted(snapshot.iterdir()):
        if not (folder / 'experiment_manifest.json').is_file():
            continue
        m = json.loads((folder / 'experiment_manifest.json').read_text())
        pid = m['identity']['parameters']['pcm_id']
        require(pid + ' accepted status', m['status'] == 'ANNUAL_NUMERICALLY_ACCEPTED')
        t = pd.read_csv(folder / 'hourly_statistics.csv', float_precision='round_trip')
        require(pid + ' annual atmospheric rows', len(t) == 8760)
        w = t.T_air_C.to_numpy()
        cutoff = np.quantile(w, 0.95, method='linear')
        require(pid + ' weather-defined extreme mask', np.array_equal(t.extreme_heat.to_numpy(), w >= cutoff))
        require(pid + ' 438 extreme hours', int(t.extreme_heat.sum()) == 438)
        with np.load(folder / 'spatial_diagnostics.npz', allow_pickle=False) as z:
            spatial = {k: z[k].copy() for k in z.files}
        require(pid + ' spatial dimensions', spatial['peak_cool_K'].shape == (93, 88))
        result = {'pcm_id': pid, 'experiment_id': folder.name, **cooling_extrema(t, spatial)}
        expected_hour, expected_cell = EXPECTED[pid]
        result['quoted_values_match_3_decimals'] = bool(abs(result['maximum_hourly_hotspot_cooling_K'] - expected_hour) < 0.0005 and abs(result['maximum_domain_grid_cell_cooling_K'] - expected_cell) < 0.0005)
        result['extreme_heat_signed_mean_K'] = float(t.loc[t.extreme_heat, 'hotspot_mean_K'].mean())
        result['extreme_heat_hours'] = int(t.extreme_heat.sum())
        result['source'] = str((folder / 'hourly_statistics.csv').relative_to(root))
        extrema.append(result)
        pair = c1 / manifest['by_pcm_directories'][pid]
        pcm = pd.read_csv(pair / 'hourly_pcm.csv', float_precision='round_trip')
        l0 = pd.read_csv(pair / 'hourly_L0.csv', float_precision='round_trip')
        dh = pd.read_csv(pair / 'delta_H.csv', float_precision='round_trip')
        require(pid + ' annual roof rows', len(pcm) == len(l0) == len(dh) == 8760)
        require(pid + ' H_PCM sign', np.array_equal(dh.H_PCM_Wm2.to_numpy(), -pcm.q_convection_mean_Wm2.to_numpy()))
        require(pid + ' H_L0 sign', np.array_equal(dh.H_L0_Wm2.to_numpy(), -l0.q_convection_mean_Wm2.to_numpy()))
        require(pid + ' delta_H equality', np.array_equal(dh.delta_H_Wm2.to_numpy(), dh.H_PCM_Wm2.to_numpy() - dh.H_L0_Wm2.to_numpy()))
        require(pid + ' paired chronology', pcm.datetime_UTC.equals(l0.datetime_UTC) and pcm.datetime_UTC.equals(dh.datetime_UTC) and pd.DatetimeIndex(pd.to_datetime(dh.datetime_UTC, utc=True)).equals(pd.DatetimeIndex(pd.to_datetime(t.datetime_UTC, utc=True))))
        meta = json.loads((pair / 'metadata.json').read_text())
        different = [k for k in meta['material'] if meta['material'][k] != meta['control_material'][k]]
        require(pid + ' matched L=0', different == ['L_Jkg'] and meta['control_material']['L_Jkg'] == 0)
        for case in ('pcm', 'L0'):
            with np.load(pair / ('cell_states_' + case + '.npz'), allow_pickle=False) as z:
                require(pid + '/' + case + ' complete depth states', z['T_C'].shape == (8761, 10))
        convergence = pd.read_csv(folder / 'numerical_convergence.csv')
        require(pid + ' saved numerical acceptance', convergence['pass'].all())
    require('All three materials present', {x['pcm_id'] for x in extrema} == set(EXPECTED))
    import rasterio
    with rasterio.open(root / 'data/inputs/geospatial/HOTSPOT_MASK.tif') as ds:
        require('Saved hotspot has 44 cells', int(np.sum(ds.read(1) == 1)) == 44)
    return {'status': 'PASS', 'scientific_solvers_invoked': False, 'checks': checks, 'extrema': extrema,
            'quoted_maxima_all_verified': all(x['quoted_values_match_3_decimals'] for x in extrema),
            'limitation': 'Saved relationships verified. This is not a new full-year equivalence run or empirical validation.'}
