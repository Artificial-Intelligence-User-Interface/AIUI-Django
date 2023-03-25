from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
import arff
import joblib
import os
from django.conf import settings

#used documentation https://scikit-learn.org/stable/modules/neural_networks_supervised.html
def trainMLP(data,model,project):
    dataDict = {}
    with open(data) as f:
        dataDict = arff.load(f)
        f.close()
    arffData = np.array(dataDict['data'])
    X = arffData[:, :-1]
    Y = arffData[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3,random_state=109)
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    # recall = metrics.recall_score(y_test, y_pred)
    pathDir = os.path.join( settings.BASE_DIR, f"aigateway/static/aigateway/{project}/{model}/")
    if(not os.path.exists(pathDir)):
            os.makedirs(pathDir)
    model_file = joblib.dump(clf,pathDir + f"{project}_{model}_mlp.joblib")
    return [accuracy, pathDir + f"{project}_{model}_mlp.joblib"]

def runMLP(data,file):
    clf = joblib.load(file)
    return clf.predict(data)