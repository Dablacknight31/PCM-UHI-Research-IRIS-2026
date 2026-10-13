"""Use original plot definitions on saved data in a new output directory.

This adapter does not reconstruct the seven later graphics with missing original
generators. No model is run. Published figure assets are never overwritten.
"""
from pathlib import Path
import argparse,json,sys
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import research_model as model

def plot_saved(experiment, output):
    experiment,output=Path(experiment).resolve(),Path(output).resolve()
    root=model.REPOSITORY_ROOT.resolve()
    if output.is_relative_to(root/'figures') or output.is_relative_to(root/'results') or output==experiment:
        raise ValueError('Choose a new output directory outside finalized figures and saved research results.')
    m=json.loads((experiment/'experiment_manifest.json').read_text())
    if m['status']!='ANNUAL_NUMERICALLY_ACCEPTED':raise ValueError('Only accepted annual baselines are supported.')
    table=pd.read_csv(experiment/'hourly_statistics.csv',float_precision='round_trip')
    table['datetime_UTC']=pd.to_datetime(table.datetime_UTC,utc=True)
    with np.load(experiment/'spatial_diagnostics.npz',allow_pickle=False) as z:
        fields={k:z[k].copy() for k in ('mean_K','peak_cool_K','peak_warm_K')}
    identity=m['identity']
    baseline=json.loads((root/'results/category3/accepted_baselines/stage_C_annual.json').read_text())
    config=json.loads((root/'configs/accepted_baseline.json').read_text())
    if baseline['coverage']!=1 or identity['hours']!=8760 or baseline['buffer_m']!=config['domain_buffer_m']:
        raise ValueError('Expected the recorded full-coverage baseline and domain.')
    # The manifest stores layout/domain identity hashes; the annual receipt
    # records full coverage, and the extracted config records the saved bounds.
    result={'folder':str(output),'hours':8760,'domain':{'bounds':config['domain_bounds_m']},
            'params':identity['parameters'],'layout':{'arrangement':'all_roofs','coverage':baseline['coverage']},'hourly':table,'summary':m['summary'],
            'mean_field_K':fields['mean_K'],'peak_cool_field_K':fields['peak_cool_K'],'peak_warm_field_K':fields['peak_warm_K']}
    output.mkdir(parents=True,exist_ok=False)
    model.c3_plot_result(result)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('experiment',type=Path)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();plot_saved(a.experiment,a.output)
if __name__=='__main__':main()
