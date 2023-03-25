from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
import joblib
#used tutorial https://www.datacamp.com/tutorial/svm-classification-scikit-learn-python
def trainSVM(data,name,model,project):
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.3,random_state=109)
    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    precision = metrics.precision_score(y_test, y_pred)
    # recall = metrics.recall_score(y_test, y_pred)
    model_file = joblib.dump(clf,f"{project}_{model}_svm.joblib")
    return model_file, accuracy, precision
def runSVM(data,file):
    clf = joblib.load(file)
    return clf.predict(data)