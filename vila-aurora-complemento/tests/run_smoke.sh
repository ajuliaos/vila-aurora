#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 monitoramento/regras.py < monitoramento/eventos_teste.jsonl > /tmp/alertas.jsonl
test "$(wc -l < /tmp/alertas.jsonl)" -eq 4
cat /tmp/alertas.jsonl | python3 resposta/responder.py > /tmp/tickets.jsonl
test "$(wc -l < /tmp/tickets.jsonl)" -eq 4
python3 ia/treinar_anomalias.py > /tmp/metricas.json
python3 -m py_compile dashboard/app.py monitoramento/regras.py resposta/responder.py ia/treinar_anomalias.py seguranca/sqli_lab.py forense/coletar_hashes.py
echo 'Smoke tests concluídos: regras, tickets, IA e sintaxe.'
