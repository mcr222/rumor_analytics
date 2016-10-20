from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from numpy import asarray
from IPython.consoleapp import classes
import csv
from numpy.core.test_rational import numerator
from pyasn1_modules.rfc2314 import Attributes

def openFile():
    with open('TS4.csv', 'rb') as f:
            reader=csv.reader(f,delimiter=';')
            instances=[]
            next(reader)
            Y=[]
            for row in reader:
                instance=row[4:]
                instances.append(instance)
                Y.append(row[3])
    return instances, Y
def transformMatrixToNum(X):
    x_array=asarray(X)
    list_classes=[]
    x_trans=[]
    x_new_trans=[]
    encoders=[]
    for cols in range(0, len(X[0])):
        encoders.append(preprocessing.LabelEncoder())        
        encoders[cols].fit_transform(x_array[:,cols])
    for i in range(0, len(X)):
        list1=[]
        for j in range(0, len(X[0])):
            f=[x_array[i,j]]
            a=encoders[j].transform(f)
            list1.append(a[0])
        x_trans.append(list1)
    return x_trans


#print allAttributes
def makeNumericMatrix(X):
    columns1to5 = [row[0:5] for row in X]
    #print columns1to6
    numericCols1=transformMatrixToNum(columns1to5)
    columns6to12= [row[5:11] for row in X]
    #print columns6to12
    numericCols2 = [[int(column) for column in row] for row in columns6to12]
    numericMatrix=[]
    #print numericCols1
    i=0
    for row1 in numericCols1:
            newRow=row1+numericCols2[i]
            i=i+1
            numericMatrix.append(newRow)
    return numericMatrix

allAttributes= openFile()
x=['NO','YES','NO','NO','NO','0','0','35274','41788','21566']
allAttributes[0].append(x)
attributes=makeNumericMatrix(allAttributes[0])
xNum=[attributes[-1]]
del attributes[-1]
clf = RandomForestClassifier(n_estimators=100)
Y=allAttributes[1]
clf = clf.fit(attributes,Y)
X_Score=  clf.score(attributes, Y)
X_random = clf.predict(xNum)
X_prob=clf.predict_proba(xNum)
x_path=clf.decision_path(xNum)
print(X_random)
print(X_Score)
print(X_prob)
print(x_path)
#print attributes
