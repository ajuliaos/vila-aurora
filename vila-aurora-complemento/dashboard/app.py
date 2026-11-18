from flask import Flask,render_template,request,redirect,session,url_for,jsonify,abort
from werkzeug.security import generate_password_hash,check_password_hash
from pathlib import Path
from functools import wraps
import sqlite3,os,json
required=['VILA_SECRET_KEY','VILA_OPERADOR_PASSWORD','VILA_AUDITOR_PASSWORD']
missing=[x for x in required if not os.getenv(x)]
if missing:raise RuntimeError('Variaveis obrigatorias ausentes: '+', '.join(missing))
app=Flask(__name__);app.secret_key=os.environ['VILA_SECRET_KEY']
app.config.update(SESSION_COOKIE_HTTPONLY=True,SESSION_COOKIE_SAMESITE='Strict',PERMANENT_SESSION_LIFETIME=1800)
DB=Path.home()/'vila-aurora-lite/data/nuvem.db'
USERS={'operador':{'hash':generate_password_hash(os.environ['VILA_OPERADOR_PASSWORD']),'role':'operador'},'auditor':{'hash':generate_password_hash(os.environ['VILA_AUDITOR_PASSWORD']),'role':'auditor'}}
def login_required(fn):
 @wraps(fn)
 def inner(*a,**k):
  if 'user' not in session:return redirect(url_for('login'))
  return fn(*a,**k)
 return inner
def role_required(role):
 def deco(fn):
  @wraps(fn)
  def inner(*a,**k):
   if session.get('role')!=role:abort(403)
   return fn(*a,**k)
  return inner
 return deco
@app.after_request
def headers(resp):
 resp.headers['X-Frame-Options']='DENY';resp.headers['X-Content-Type-Options']='nosniff';resp.headers['Referrer-Policy']='no-referrer'
 return resp
@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='POST':
  u=request.form.get('username','');p=request.form.get('password','')
  if u in USERS and check_password_hash(USERS[u]['hash'],p):session.clear();session['user']=u;session['role']=USERS[u]['role'];return redirect(url_for('index'))
  return render_template('login.html',erro='Credenciais inválidas'),401
 return render_template('login.html')
@app.get('/logout')
def logout():session.clear();return redirect(url_for('login'))
@app.get('/')
@login_required
def index():
 events=[]
 if DB.exists():
  with sqlite3.connect(DB) as c:
   try:events=c.execute('SELECT id,ts,payload FROM eventos ORDER BY ts DESC LIMIT 50').fetchall()
   except sqlite3.Error:events=[]
 parsed=[]
 for eid,ts,payload in events:
  try:d=json.loads(payload)
  except Exception:d={'raw':payload}
  parsed.append({'id':eid,'ts':ts,'payload':d})
 return render_template('index.html',eventos=parsed,user=session['user'],role=session['role'])
@app.get('/admin')
@login_required
@role_required('operador')
def admin():return jsonify(status='área restrita de operação')
if __name__=='__main__':app.run(host='10.77.0.1',port=8080)
