from pathlib import Path
import hashlib,csv,datetime,sys
base=Path(sys.argv[1] if len(sys.argv)>1 else 'evidencias')
rows=[]
for p in sorted(base.rglob('*')):
 if p.is_file() and p.name!='manifesto_sha256.csv':
  h=hashlib.sha256(p.read_bytes()).hexdigest();rows.append([str(p),h,datetime.datetime.now(datetime.timezone.utc).isoformat()])
with (base/'manifesto_sha256.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['arquivo','sha256','coletado_em_utc']);w.writerows(rows)
print('arquivos registrados:',len(rows))
