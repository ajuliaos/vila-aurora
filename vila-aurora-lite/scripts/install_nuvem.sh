#!/usr/bin/env bash
set -euo pipefail
sudo apt update
sudo apt install -y python3-flask sqlite3 wireguard
mkdir -p "$HOME/vila-aurora-lite/data" "$HOME/vila-aurora-lite/logs"
python3 -c "import flask;print('Dependências da nuvem OK')"
