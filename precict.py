import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pickle import dump, load
import warnings
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
warnings.simplefilter("ignore")

df = pd.read_csv("C:/Users/Admin/Desktop/final_test/final_test.csv")
treatment = {
    'weight': 0.0,
    'age': round(np.nanmean(df['age']), 2),
    'height': round(np.nanmean(df['height']), 2)
}
df = df.fillna(value=treatment)
df['size'] = df['size'].map({'XXS': 1, 'S': 2, "M" : 3, "L" : 4, "XL" : 5, "XXL" : 6, "XXXL" : 7})
X = df.drop("size", axis=1)
y = df["size"]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

clf1 = KNeighborsClassifier(42)
clf1.fit(X_train,y_train)

dump(clf1, open("C:/Users/Admin/Desktop/final_test/predict.pkl","wb"))





