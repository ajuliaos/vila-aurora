import json,time,requests,sys,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from buffer import connect
URL=os.getenv("VILA_API_URL","http://10.77.0.1:5000/eventos")
TOKEN=os.environ["VILA_API_TOKEN"]
HEADERS={"Authorization":f"Bearer {TOKEN}"}
while True:
    with connect() as c:
        rows=c.execute("SELECT id,ts,payload FROM eventos WHERE synced=0 ORDER BY ts LIMIT 50").fetchall()
    for eid,ts,payload in rows:
        try:
            r=requests.post(URL,headers=HEADERS,json={"id":eid,"ts":ts,"payload":json.loads(payload)},timeout=5)
            if r.status_code==409:
                print("CONFLITO de UUID:",eid,flush=True); continue
            r.raise_for_status(); body=r.json()
            if body.get("stored") and body.get("id")==eid:
                with connect() as c:c.execute("UPDATE eventos SET synced=1 WHERE id=?",(eid,))
        except (requests.RequestException,ValueError) as e:
            print("Nuvem indisponível; eventos preservados:",type(e).__name__,flush=True);break
    print("lote_pendente",len(rows),flush=True);time.sleep(10)
