"""Check packaged files and saved baselines without importing or running a model."""
from pathlib import Path
import argparse,ast,csv,hashlib,json,math,re,sys
from urllib.parse import unquote,urlsplit

MODEL_SHA256='d584d798eb74eb24076b37e34cea783b38c98de37eb361cbf14285c01ddf819c'
EXPECTED={'PCM-011':(0.456324687826,0.697010701462),'PCM-067':(0.500685497998,0.796938813589),'PCM-069':(0.502713612937,0.819003907026)}
GENERATED={'manifests/repository_file_manifest.csv','manifests/repository_file_manifest.sha256'}
REQUIRED=['README.md','REPRODUCIBILITY.md','DATA_AVAILABILITY.md','THIRD_PARTY_NOTICES.md','PAPER_FIGURE_INDEX.md','docs/methodology.md','docs/research_workflow.md','docs/model_assumptions.md','docs/limitations.md','docs/public_release_scope.md','docs/scientific_provenance.md','src/research_model.py','requirements.txt','requirements.lock.txt','configs/accepted_baseline.json','configs/input_locations.json','manifests/public_figure_provenance.csv','manifests/dependency_provenance.json']

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def rows(p):
 with p.open(newline='') as f:return list(csv.DictReader(f))

def verify(root,saved=False):
 root=Path(root).resolve();checks=[];warnings=[]
 def check(name,ok):checks.append({'check':name,'passed':bool(ok)})
 files=[p for p in root.rglob('*') if p.is_file() and not any(x in p.relative_to(root).parts for x in ['.git','.venv','runtime','__pycache__','.pcm_uhi_cache'])]
 paths={p.relative_to(root).as_posix():p for p in files}
 check('Required documentation and model',all(x in paths for x in REQUIRED))
 check('Model matches distributed source checksum',digest(root/'src/research_model.py')==MODEL_SHA256)
 syntax=[]
 for p in root.glob('src/**/*.py'):
  try:compile(p.read_text(),str(p),'exec')
  except Exception as e:syntax.append({'path':p.relative_to(root).as_posix(),'error':str(e)})
 check('Python source syntax in memory',not syntax)
 oversized=[{'path':k,'bytes':p.stat().st_size} for k,p in paths.items() if p.stat().st_size>25*1024*1024]
 check('No selected file exceeds conservative 25 MiB review threshold',not oversized)
 git_present=(root/'.git').exists()
 banned=[k for k in paths if Path(k).name in {'.DS_Store','.env'} or Path(k).suffix in {'.pyc','.pkl','.pickle','.zip'} or any(x in k.split('/') for x in ['.venv','.python-runtime','.local_cache','.config'])]
 check('No runtime/cache/private archive artifacts',not banned)
 broken=[];links=0
 for k,p in paths.items():
  if p.suffix!='.md':continue
  text=p.read_text();text=re.sub(r'```.*?```','',text,flags=re.S)
  for target in re.findall(r'!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)',text):
   target=target.strip('<>');u=urlsplit(target)
   if u.scheme or u.netloc or target.startswith('#'):continue
   links+=1;dest=p.parent/re.sub(r':\d+$','',unquote(u.path))
   if not dest.exists():broken.append({'document':k,'target':target})
 check('Markdown relative file links',not broken)
 findings=[];absolute_code=[];private_paths=[];scanned=0
 patterns={
  'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
  'github_token':r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b',
  'google_api_key':r'\bAIza[A-Za-z0-9_-]{35}\b',
  'aws_access_key':r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
  'literal_secret_assignment':r'''(?i)(?:api_key|access_token|refresh_token|client_secret|password)\s*[=:]\s*["'][A-Za-z0-9/+_.=-]{16,}["']'''}
 for k,p in paths.items():
  if p.suffix not in {'.md','.py','.json','.csv','.log','.txt','.sha256','.geojson'} and p.name!='.gitignore':continue
  scanned+=1
  for num,line in enumerate(p.read_text(errors='replace').splitlines(),1):
   for label,pat in patterns.items():
    if re.search(pat,line):findings.append({'path':k,'line':num,'kind':label})
   if re.search(r'/(?:Users|home)/[A-Za-z0-9_.-]+/|[A-Z]:\\Users\\',line):
    private_paths.append({'path':k,'line':num})
    if k.startswith('src/'):absolute_code.append({'path':k,'line':num})
 check('Pattern-based credential scan',not findings)
 check('No machine-specific execution paths in source',not absolute_code)
 check('No personal absolute paths in public text or metadata',not private_paths)
 check('No personal absolute paths in public text or metadata',not private_paths)
 check('No personal absolute paths in public text or metadata',not private_paths)
 check('No personal absolute paths in public text or metadata',not private_paths)
 manifest=root/'manifests/repository_file_manifest.csv';mismatch=[];coverage=[];sealed=0
 if manifest.exists():
  mrows=rows(manifest);sealed=len(mrows)
  for r in mrows:
   p=root/r['repository_path']
   if not p.is_file() or p.stat().st_size!=int(r['file_size_bytes']) or digest(p)!=r['sha256']:mismatch.append(r['repository_path'])
  declared={r['repository_path'] for r in mrows}
  coverage=sorted((set(paths)-GENERATED)-declared)+sorted(declared-set(paths))
  seal=(root/'manifests/repository_file_manifest.sha256').read_text().split()[0]
  check('Detached file-manifest seal',seal==digest(manifest))
  check('All declared file checksums and sizes',not mismatch)
  check('Manifest membership matches actual included files',not coverage and len(declared)==len(mrows))
 else:check('Publication manifest exists',False)
 t=ast.parse((root/'src/research_model.py').read_text())
 func=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='select_persistent_hotspot'][0]
 code=ast.get_source_segment((root/'src/research_model.py').read_text(),func)
 check('Protected shared-edge selector and ranking retained',all(x in code for x in ['cfg[\'connectivity\'] == 4','(r - 1, c)', '(r + 1, c)', '(r, c - 1)', '(r, c + 1)','minimum_component_cells','built_weighted_area_m2','mean_pre_excess_C']))
 scientific=[]
 if saved:
  import numpy as np
  summary=rows(root/'results/category1/annual_summary.csv')
  screening=rows(root/'results/postprocessing/baseline_graphs/candidate_screen_audit.csv')
  check('32 screened model-ready rows and three inclusive passes',len(screening)==77 and sum(r['section0_readiness']=='RUNNABLE_SCHEMA_ONLY' for r in screening)==32 and {r['pcm_id'] for r in screening if r['pass'].lower()=='true'}==set(EXPECTED))
  cm=json.loads((root/'results/category1/category1_manifest.json').read_text())
  actual=set()
  for folder in sorted((root/'results/category3/accepted_baselines').iterdir()):
   if not (folder/'experiment_manifest.json').is_file():continue
   m=json.loads((folder/'experiment_manifest.json').read_text());pid=m['identity']['parameters']['pcm_id'];actual.add(pid)
   if pid not in EXPECTED:check('No unexpected accepted material '+pid,False);continue
   h=rows(folder/'hourly_statistics.csv');means=np.array([float(r['hotspot_mean_K']) for r in h]);air=np.array([float(r['T_air_C']) for r in h]);ext=np.array([r['extreme_heat'].lower()=='true' for r in h])
   with np.load(folder/'spatial_diagnostics.npz',allow_pickle=False) as z:
    maximum=max(0.,-float(np.min(z['peak_cool_K'])));shape=z['peak_cool_K'].shape;source=z['source'].copy();weights=z['weights'].copy()
   hourly=max(0.,-float(means.min()));cellhour=max(float(r['hotspot_max_cooling_K']) for r in h)
   check(pid+' accepted annual statistics/compact spatial dimensions',m['status']=='ANNUAL_NUMERICALLY_ACCEPTED' and len(h)==8760 and shape==(93,88))
   check(pid+' hourly hotspot maximum preserved to 1e-12',abs(hourly-EXPECTED[pid][0])<1e-12)
   check(pid+' independent instantaneous-cell maxima preserved to 1e-12',abs(maximum-EXPECTED[pid][1])<1e-12 and abs(cellhour-maximum)<1e-12)
   check(pid+' weather-defined 438 extreme hours',int(ext.sum())==438 and np.array_equal(ext,air>=np.quantile(air,.95)))
   pair=root/'results/category1'/cm['by_pcm_directories'][pid]
   a,b,dh=[rows(pair/n) for n in ['hourly_pcm.csv','hourly_L0.csv','delta_H.csv']]
   check(pid+' paired annual chronology',len(a)==len(b)==len(dh)==len(h)==8760 and all(x['datetime_UTC']==y['datetime_UTC']==d['datetime_UTC']==v['datetime_UTC'] for x,y,d,v in zip(a,b,dh,h)))
   check(pid+' sensible forcing signs and exact differences',all(float(d['H_PCM_Wm2'])==-float(x['q_convection_mean_Wm2']) and float(d['H_L0_Wm2'])==-float(y['q_convection_mean_Wm2']) and float(d['delta_H_Wm2'])==float(d['H_PCM_Wm2'])-float(d['H_L0_Wm2']) for x,y,d in zip(a,b,dh)))
   meta=json.loads((pair/'metadata.json').read_text());diff=[k for k in meta['material'] if meta['material'][k]!=meta['control_material'][k]]
   check(pid+' latent-only matched control',diff==['L_Jkg'] and meta['control_material']['L_Jkg']==0)
   for case in ['pcm','L0']:
    with np.load(pair/('cell_states_'+case+'.npz'),allow_pickle=False) as z:check(pid+'/'+case+' saved full depth states',z['T_C'].shape==(8761,10))
   check(pid+' saved convergence flags',all(r['pass'].lower()=='true' for r in rows(folder/'numerical_convergence.csv')))
   area=float(weights[0].sum());treated=float((source*22500).sum())
   check(pid+' selected hotspot and treated geometry',abs(area-990000)<1e-6 and abs(treated-344120.4951360407)<1e-6)
   scientific.append({'pcm_id':pid,'maximum_hourly_hotspot_cooling_C':hourly,'maximum_instantaneous_grid_cell_cooling_C':maximum,'signed_annual_mean_hotspot_anomaly_C':float(means.mean()),'hottest_weather_subset_mean_anomaly_C':float(means[ext].mean()),'treated_area_m2':treated})
  check('All and only three accepted materials',actual==set(EXPECTED))
 return {'status':'PASS' if all(r['passed'] for r in checks) else 'FAIL','scope':'Packaging and optional saved numerical relationships; no scientific simulation','scientific_solvers_invoked':False,'git_directory_present':git_present,'checks':checks,'markdown_links_checked':links,'broken_links':broken,'syntax_errors':syntax,'checksum_mismatches':mismatch,'membership_mismatches':coverage,'sealed_files':sealed,'oversized_files':oversized,'secret_scan':{'text_files_scanned':scanned,'findings':findings,'limitation':'Pattern scan only; author attribution and scientific run identities remain public.'},'absolute_code_paths':absolute_code,'personal_path_findings':private_paths,'personal_path_findings':private_paths,'personal_path_findings':private_paths,'personal_path_findings':private_paths,'saved_metrics':scientific,'warnings':warnings}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);p.add_argument('--saved',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args();root=a.root.resolve()
 result=verify(root,a.saved)
 if a.output:
  out=a.output.resolve()
  if out.is_relative_to(root) and not out.is_relative_to(root/'runtime'):raise ValueError('Write verification receipts to runtime/ or outside the sealed repository.')
  out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2));return 0 if result['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
