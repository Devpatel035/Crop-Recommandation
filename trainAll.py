import pandas as pd
data=pd.read_csv("Crop_recommendation.csv")
data=data.dropna(how='any')
colums=data.columns
X=data.loc[:,colums[:7]]
y=data.loc[:,colums[7]]

#array Conver
X=X.to_numpy()
#label Encoding
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(y)
y=le.transform(y)
import pickle
pickle.dump(le, open('le.pkl', 'wb'))

#spilit data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

import warnings
warnings.filterwarnings("ignore")
names = ["Nearest Neighbors", "Liner SVM",
         "Decision Tree", "Random Forest",
         "Naive Bayes","ExtraTreesClassifier"]
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
classifiers = [
    make_pipeline(Normalizer(),KNeighborsClassifier()),
    make_pipeline(Normalizer(),LinearSVC()),
    make_pipeline(Normalizer(),DecisionTreeClassifier()),
    make_pipeline(Normalizer(),RandomForestClassifier()),
    make_pipeline(Normalizer(),GaussianNB()),
    make_pipeline(Normalizer(),ExtraTreesClassifier())]
clfF=[]
for name, clf in zip(names, classifiers):
    clf.fit(X_train, y_train)
    import bz2
    sfile = bz2.BZ2File(name, 'w')
    pickle.dump(clf, sfile)
    # Add loop for checking every patient file and save results
    y_pred=clf.predict(X_test)
    #y_mod print max value as final class
    clfF.append(clf)
    print(name)
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print('--------------------------------------------------------------')
sfile = bz2.BZ2File("All Model", 'w')
pickle.dump(clfF, sfile)   
    
    
    
    
    
    
    
    
    
    
    