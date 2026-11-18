"""Laboratório local e isolado. A rota vulnerável só existe se LAB_VULNERAVEL=1."""
from flask import Flask,request,jsonify
import sqlite3,os
app=Flask(__name__); DB='sqli_lab.db'
with sqlite3.connect(DB) as c:
 c.execute('CREATE TABLE IF NOT EXISTS pessoas(id INTEGER PRIMARY KEY,nome TEXT)');c.execute("INSERT OR IGNORE INTO pessoas VALUES(1,'Exemplo')")
@app.get('/seguro')
def seguro():
 q=request.args.get('nome','')
 with sqlite3.connect(DB) as c:r=c.execute('SELECT id,nome FROM pessoas WHERE nome=?',(q,)).fetchall()
 return jsonify(r)
if os.environ.get('LAB_VULNERAVEL')=='1':
 @app.get('/vulneravel')
 def vulneravel():
  q=request.args.get('nome','')
  with sqlite3.connect(DB) as c:r=c.execute("SELECT id,nome FROM pessoas WHERE nome='"+q+"'").fetchall()
  return jsonify(r)
if __name__=='__main__':app.run(host='127.0.0.1',port=5050)
