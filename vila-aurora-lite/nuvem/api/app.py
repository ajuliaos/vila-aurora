from flask import Flask,request,jsonify
import sqlite3,json
from pathlib import Path
app=Flask(__name__); DB=Path.home()/"vila-aurora-lite/data/nuvem.db"; DB.parent.mkdir(parents=True,exist_ok=True)
def init():
    with sqlite3.connect(DB) as c: c.execute("CREATE TABLE IF NOT EXISTS eventos(id TEXT PRIMARY KEY, ts TEXT NOT NULL, payload TEXT NOT NULL)")
init()
@app.get("/health")
def health(): return jsonify(status="ok")
@app.post("/eventos")
def eventos():
    d=request.get_json(silent=True)
    if not isinstance(d,dict) or not all(k in d for k in ("id","ts","payload")): return jsonify(error="payload invalido"),400
    with sqlite3.connect(DB) as c: c.execute("INSERT OR IGNORE INTO eventos VALUES(?,?,?)",(str(d["id"]),str(d["ts"]),json.dumps(d["payload"])))
    return jsonify(id=d["id"],stored=True),200
@app.get("/eventos/count")
def count():
    with sqlite3.connect(DB) as c: n=c.execute("SELECT COUNT(*) FROM eventos").fetchone()[0]
    return jsonify(count=n)
if __name__=="__main__": app.run(host="10.77.0.1",port=5000)
