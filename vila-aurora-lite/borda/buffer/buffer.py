import sqlite3, uuid, json
from datetime import datetime, timezone
from pathlib import Path
DB=Path.home()/"vila-aurora-lite/data/eventos.db"
DB.parent.mkdir(parents=True,exist_ok=True)
def connect():
    c=sqlite3.connect(DB,timeout=10)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("CREATE TABLE IF NOT EXISTS eventos(id TEXT PRIMARY KEY, ts TEXT NOT NULL, payload TEXT NOT NULL, synced INTEGER DEFAULT 0)")
    c.commit(); return c
def gravar(payload):
    eid=str(uuid.uuid4())
    with connect() as c:
        c.execute("INSERT INTO eventos(id,ts,payload) VALUES(?,?,?)",(eid,datetime.now(timezone.utc).isoformat(),json.dumps(payload)))
    return eid
