#!/usr/bin/env bash
set -euo pipefail
sudo apt update
sudo apt install -y python3-paho-mqtt python3-requests sqlite3 wireguard
mkdir -p "$HOME/vila-aurora-lite/data" "$HOME/vila-aurora-lite/logs"
python3 -c "import paho.mqtt.client,requests;print('Dependências da borda OK')"
sudo systemctl is-active mosquitto
