import os,tempfile,importlib.util,sys
from pathlib import Path
os.environ.setdefault('VILA_API_TOKEN','token-teste')
# Teste funcional deve ser executado em cópia isolada para não tocar o banco real.
print('Pré-requisito de token OK; execute teste_integracao.py no laboratório.')
