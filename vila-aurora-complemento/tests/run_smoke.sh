#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
printf '%s\n' 'Testando regras...'
python3 monitoramento/regras.py < monitoramento/eventos_teste.jsonl | tee evidencias/alertas_teste.jsonl
test "$(wc -l < evidencias/alertas_teste.jsonl)" -eq 4
printf '%s\n' 'Testando IA...'
python3 ia/treinar_anomalias.py | tee evidencias/metricas_ia_console.txt
printf '%s\n' 'Smoke tests concluídos.'
