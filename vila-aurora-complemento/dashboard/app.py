from flask import Flask, render_template, request, redirect, session, url_for, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
import sqlite3, os, json
app=Flask(__name__)
app.secret_key=os.environ['VILA_SECRET_KEY']
DB=Path.home()/ 'vila-aurora-lite/data/nuvem.db'
USERS={
 'operador': {'hash':generate_password_hash(os.environ['VILA_OPERADOR_PASSWORD']),'role':'operador'},
 'auditor': {'hash':generate_password_hash(os.environ['VILA_AUDITOR_PASSWORD']),'role':'auditor'}
}
def need_login(fn):
 from functools import wraps
 @wraps(fn)
 def inner(*a,**k):
  if 'user' not in session:return redirect(url_for('login'))
  return fn(*a,**k)
 return inner
@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='POST':
  u=request.form.get('username','');p=request.form.get('password','')
  if u in USERS and check_password_hash(USERS[u]['hash'],p):
   session.clear();session['user']=u;session['role']=USERS[u]['role'];return redirect(url_for('index'))
  return render_template('login.html',erro='Credenciais invÃ¡lidas'),401
 return render_template('login.html')
@app.get('/logout')
def logout():session.clear();return redirect(url_for('login'))
@app.get('/')
@need_login
def index():
 eventos=[]
 if DB.exists():
  with sqlite3.connect(DB) as c:
   try:eventos=c.execute('SELECT id,ts,payload FROM eventos ORDER BY ts DESC LIMIT 50').fetchall()
   except sqlite3.Error:eventos=[]
 parsed=[]
 for eid,ts,payload in eventos:
  try:d=json.loads(payload)
  except Exception:d={'raw':payload}
  parsed.append({'id':eid,'ts':ts,'payload':d})
 return render_template('index.html',eventos=parsed,user=session['user'],role=session['role'])
@app.get('/api/summary')
@need_login
def summary():
 total=0
 if DB.exists():
  with sqlite3.connect(DB) as c:
   try:total=c.execute('SELECT COUNT(*) FROM eventos').fetchone()[0]
   except sqlite3.Error:pass
 return jsonify(total=total,role=session['role'])
@app.get('/admin')
@need_login
def admin():
 if session.get('role')!='operador':abort(403)
 return jsonify(status='Ã¡rea restrita de operaÃ§Ã£o')
if __name__=='__main__':
 app.run(host='10.77.0.1',port=8080)
