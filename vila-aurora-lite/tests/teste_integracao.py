import os,sqlite3,requests
from pathlib import Path
url=os.getenv('VILA_API_BASE','http://10.77.0.1:5000')
h={'Authorization':f"Bearer {os.environ['VILA_API_TOKEN']}"}
assert requests.get(url+'/health',timeout=5).json()['status']=='ok'
remote=requests.get(url+'/eventos/count',headers=h,timeout=5);remote.raise_for_status()
p=Path.home()/"vila-aurora-lite/data/eventos.db"
with sqlite3.connect(p) as c:
    pending=c.execute("SELECT COUNT(*) FROM eventos WHERE synced=0").fetchone()[0]
    total=c.execute("SELECT COUNT(*) FROM eventos").fetchone()[0]
assert pending==0, f"eventos pendentes: {pending}"
assert remote.json()['count']==total,(remote.json()['count'],total)
print('Integração OK:',total,'eventos; zero pendentes')
