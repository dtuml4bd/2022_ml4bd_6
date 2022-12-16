from pickle import load
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

loaded_model = load(open('D:/test/flaskblog/predict.pkl', 'rb'))
features = (["weight","age","height"])
Du_lieu=[60,25,160]

x_pred_sample1 = np.array(Du_lieu).reshape(1,-1)
t = loaded_model.predict(x_pred_sample1)
if t == 1: 
    decision ="XXS" 
if t ==2:
    decision ="S" 
if t ==3:
    decision ="L" 
if t ==4: 
    decision ="M" 
if t ==5:
    decision ="X"  
if t ==6:
    decision ="XXL"  
print(f"Điểm dữ liệu ở vị trí {x_pred_sample1} Thuộc lớp {decision}")
