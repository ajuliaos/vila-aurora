from pathlib import Path
import numpy as np,json,csv,joblib
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix,precision_score,recall_score
rng=np.random.default_rng(2026)
def normal(n):return np.column_stack((rng.normal(5,1,n),rng.normal(100,20,n),rng.poisson(1,n)))
def anomaly(n):return np.column_stack((rng.choice([-5,20],n)+rng.normal(0,2,n),rng.normal(700,140,n),rng.integers(7,18,n)))
train=normal(700);test=np.vstack((normal(300),anomaly(50)));y=np.array([0]*300+[1]*50)
model=IsolationForest(contamination=.08,random_state=2026).fit(train);pred=(model.predict(test)==-1).astype(int);cm=confusion_matrix(y,pred)
metrics={'dataset':'synthetic_holdout','train_rows':len(train),'test_rows':len(test),'matrix':cm.tolist(),'precision':float(precision_score(y,pred,zero_division=0)),'recall':float(recall_score(y,pred,zero_division=0)),'false_positive_rate':float(cm[0,1]/sum(cm[0]))}
out=Path(__file__).resolve().parent/'saida';out.mkdir(exist_ok=True);joblib.dump(model,out/'modelo.joblib');(out/'metricas_holdout.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
with (out/'previsoes_holdout.csv').open('w',newline='',encoding='utf-8') as f:
 writer=csv.writer(f);writer.writerow(['temperatura','latencia_ms','tentativas','real_anomalia','pred_anomalia']);writer.writerows([*map(float,x),int(a),int(b)] for x,a,b in zip(test,y,pred))
print(json.dumps(metrics,indent=2))
