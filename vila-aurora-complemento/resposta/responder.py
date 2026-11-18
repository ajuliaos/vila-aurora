import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent / "tickets.jsonl"

for line in sys.stdin:
    if not line.strip():
        continue
    event = json.loads(line)
    severity = event.get("severity", "medio")
    ticket = {
        "id": str(uuid.uuid4()),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "rule": event.get("rule", "UNKNOWN"),
        "severity": severity,
        "status": "AGUARDANDO_ANALISE",
        "action": "NOTIFICAR_OPERADOR",
        "requires_human_approval": severity in ("alto", "critico"),
        "source_event": event,
    }
    with OUT.open("a", encoding="utf-8") as output:
        output.write(json.dumps(ticket, ensure_ascii=False) + "\n")
    print(json.dumps(ticket, ensure_ascii=False))
