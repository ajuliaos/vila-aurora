from pathlib import Path
import numpy as np,pandas as pd,joblib,json
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix,precision_score,recall_score
R=np.random.default_rng(42); n=1000
normal=pd.DataFrame({'temperatura':R.normal(5,1,n),'latencia_ms':R.normal(100,20,n),'tentativas':R.poisson(1,n),'label':0})
anom=pd.DataFrame({'temperatura':R.choice([-5,20],50)+R.normal(0,1,50),'latencia_ms':R.normal(800,100,50),'tentativas':R.integers(8,20,50),'label':1})
df=pd.concat([normal,anom],ignore_index=True).sample(frac=1,random_state=42)
X=df[['temperatura','latencia_ms','tentativas']]
model=IsolationForest(contamination=50/1050,random_state=42).fit(X)
pred=(model.predict(X)==-1).astype(int)
metrics={'matrix':confusion_matrix(df.label,pred).tolist(),'precision':precision_score(df.label,pred),'recall':recall_score(df.label,pred),'false_positive_rate':float(((pred==1)&(df.label==0)).sum()/(df.label==0).sum())}
out=Path(__file__).resolve().parent/'saida';out.mkdir(exist_ok=True)
df.assign(pred=pred).to_csv(out/'avaliacao.csv',index=False);joblib.dump(model,out/'modelo.joblib');(out/'metricas.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8');print(json.dumps(metrics,indent=2))
