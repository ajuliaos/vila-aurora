#!/usr/bin/env bash
set -euo pipefail
sudo apt update
sudo apt install -y python3-flask python3-sklearn python3-pandas python3-matplotlib python3-joblib sqlite3
mkdir -p "$HOME/vila-aurora-complemento/evidencias"
python3 -c "import flask,sklearn,pandas,joblib;print('Dependências OK')"
