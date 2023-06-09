from sklearn import svm
import numpy as np
import arff
from sklearn.model_selection import train_test_split
from sklearn import metrics
import joblib
import os
from django.conf import settings

#used tutorial https://www.datacamp.com/tutorial/svm-classification-scikit-learn-python
def trainSVM(data,model,project, pathDir):

    dataDict = {}
    with open(data) as f:
        dataDict = arff.load(f)
        f.close()
    
    arffData = np.array(dataDict['data'])

    X = arffData[:, :-1]
    Y = arffData[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3,random_state=109)

    clf = svm.SVC(kernel='linear')

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    accuracy = metrics.accuracy_score(y_test, y_pred)
    # precision = metrics.precision_score(y_test, y_pred)
    # recall = metrics.recall_score(y_test, y_pred)
    
    model_file = joblib.dump(clf,pathDir + f"{project}_{model}_svm.joblib")
    return [accuracy, pathDir + f"{project}_{model}_svm.joblib"]

def runSVM(data,file):
    # npdata = np.array(data).reshape(1, -1)
    clf = joblib.load(file)
    return list(clf.predict([data]))