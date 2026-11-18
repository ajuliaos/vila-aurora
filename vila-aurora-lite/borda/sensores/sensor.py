import json,random,ssl,time,sys
from pathlib import Path
from datetime import datetime,timezone
import paho.mqtt.client as mqtt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"buffer"))
from buffer import gravar
HOME=Path.home(); CERTS=HOME/"mqtt-certs"
client=mqtt.Client(client_id="ubs-sensor-01")
client.tls_set(ca_certs=str(CERTS/"ca.crt"),certfile=str(CERTS/"sensor.crt"),keyfile=str(CERTS/"sensor.key"),tls_version=ssl.PROTOCOL_TLS_CLIENT)
client.connect("192.168.56.20",8883,60); client.loop_start()
try:
    while True:
        valor=round(random.uniform(1,11),2)
        event={"sensor":"ubs-01","temperatura":valor,"unidade":"C","timestamp":datetime.now(timezone.utc).isoformat()}
        eid=gravar(event)
        info=client.publish("vila/ubs/camara-fria",json.dumps(event),qos=1); info.wait_for_publish(timeout=10)
        print(json.dumps({"id":eid,"mqtt_rc":info.rc,**event}),flush=True)
        if valor<2 or valor>8: print("ALERTA_LOCAL: temperatura fora da faixa 2-8 C",flush=True)
        time.sleep(5)
except KeyboardInterrupt: pass
finally: client.loop_stop(); client.disconnect()
