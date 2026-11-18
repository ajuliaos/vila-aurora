import json,re,sys
from datetime import datetime,timezone
RULES=[
 ('MTLS_SEM_CERT',lambda e:'certificate required' in e.get('message','').lower(),'alto'),
 ('SQLI_PADRAO',lambda e:bool(re.search(r"(?i)(union\s+select|or\s+['\"]?1['\"]?=['\"]?1|sleep\s*\()",e.get('message',''))),'alto'),
 ('VPN_ATIPICA',lambda e:e.get('kind')=='vpn_login' and (e.get('hour',12)<6 or e.get('hour',12)>22),'medio'),
 ('ATUADOR_FORA_HORARIO',lambda e:e.get('kind')=='atuador' and (e.get('hour',12)<6 or e.get('hour',12)>20),'critico')]
def avaliar(event):
 out=[]
 for nome,test,severidade in RULES:
  try:
   if test(event):out.append({'rule':nome,'severity':severidade,'event':event,'detected_at':datetime.now(timezone.utc).isoformat()})
  except Exception:pass
 return out
if __name__=='__main__':
 for line in sys.stdin:
  try:
   e=json.loads(line);[print(json.dumps(x,ensure_ascii=False)) for x in avaliar(e)]
  except json.JSONDecodeError:print('linha inválida',file=sys.stderr)
