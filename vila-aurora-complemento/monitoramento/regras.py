import json
import re
import sys
from datetime import datetime, timezone

RULES = [
    (
        "MTLS_SEM_CERT",
        lambda event: "certificate required" in event.get("message", "").lower(),
        "alto",
    ),
    (
        "SQLI_PADRAO",
        lambda event: bool(
            re.search(
                r"(?i)(union\s+select|or\s+['\"]?1['\"]?\s*=\s*['\"]?1|sleep\s*\()",
                event.get("message", ""),
            )
        ),
        "alto",
    ),
    (
        "VPN_ATIPICA",
        lambda event: event.get("kind") == "vpn_login"
        and (event.get("hour", 12) < 6 or event.get("hour", 12) > 22),
        "medio",
    ),
    (
        "ATUADOR_FORA_HORARIO",
        lambda event: event.get("kind") == "atuador"
        and (event.get("hour", 12) < 6 or event.get("hour", 12) > 20),
        "critico",
    ),
]

def avaliar(event):
    alerts = []
    for name, test, severity in RULES:
        try:
            if test(event):
                alerts.append(
                    {
                        "rule": name,
                        "severity": severity,
                        "event": event,
                        "detected_at": datetime.now(timezone.utc).isoformat(),
                    }
                )
        except (TypeError, ValueError, KeyError):
            continue
    return alerts

if __name__ == "__main__":
    for line in sys.stdin:
        try:
            for item in avaliar(json.loads(line)):
                print(json.dumps(item, ensure_ascii=False))
        except json.JSONDecodeError:
            print("linha inválida", file=sys.stderr)
