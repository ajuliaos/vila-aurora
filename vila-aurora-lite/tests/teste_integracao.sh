#!/usr/bin/env bash
set -euo pipefail
ping -c 2 10.77.0.1
curl -fsS http://10.77.0.1:5000/health
curl -fsS http://10.77.0.1:5000/eventos/count
python3 - <<'PY'
import sqlite3
from pathlib import Path
p=Path.home()/"vila-aurora-lite/data/eventos.db"
with sqlite3.connect(p) as c: print("buffer_por_status",c.execute("select synced,count(*) from eventos group by synced").fetchall())
PY
