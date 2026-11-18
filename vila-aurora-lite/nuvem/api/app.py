from flask import Flask,request,jsonify
import sqlite3,json,os,hmac
from pathlib import Path
app=Flask(__name__)
DB=Path.home()/"vila-aurora-lite/data/nuvem.db";DB.parent.mkdir(parents=True,exist_ok=True)
TOKEN=os.environ["VILA_API_TOKEN"]
def init():
    with sqlite3.connect(DB) as c:c.execute("CREATE TABLE IF NOT EXISTS eventos(id TEXT PRIMARY KEY, ts TEXT NOT NULL, payload TEXT NOT NULL)")
init()
def authorized():
    value=request.headers.get("Authorization","")
    return value.startswith("Bearer ") and hmac.compare_digest(value[7:],TOKEN)
@app.get('/health')
def health():return jsonify(status='ok')
@app.post('/eventos')
def eventos():
    if not authorized():return jsonify(error='nao autorizado'),401
    d=request.get_json(silent=True)
    if not isinstance(d,dict) or set(("id","ts","payload"))-set(d):return jsonify(error='payload invalido'),400
    eid,ts,payload=str(d['id']),str(d['ts']),json.dumps(d['payload'],sort_keys=True,separators=(',',':'))
    with sqlite3.connect(DB) as c:
        old=c.execute("SELECT ts,payload FROM eventos WHERE id=?",(eid,)).fetchone()
        if old:
            if old==(ts,payload):return jsonify(id=eid,stored=True,idempotent=True),200
            return jsonify(error='uuid existente com conteudo divergente',id=eid),409
        c.execute("INSERT INTO eventos VALUES(?,?,?)",(eid,ts,payload))
    return jsonify(id=eid,stored=True,idempotent=False),201
@app.get('/eventos/count')
def count():
    if not authorized():return jsonify(error='nao autorizado'),401
    with sqlite3.connect(DB) as c:n=c.execute("SELECT COUNT(*) FROM eventos").fetchone()[0]
    return jsonify(count=n)
if __name__=='__main__':app.run(host=os.getenv('VILA_API_HOST','10.77.0.1'),port=int(os.getenv('VILA_API_PORT','5000')))
