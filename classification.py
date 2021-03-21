import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from phishing_classificaton import decision_tree_train_and_predict

data_files = ['Sources/Training_Dataset.csv', 'trainingdata.csv']

def read_data(filename):
    # Daten einlesen
    features = pd.read_csv(filename)
    # Labels extrahieren: letzte Spalte 'Result', die bestimmt ob ein Eintrag Phishing ist oder nicht
    labels = np.array(features['Result'])
    # Spalte mit den Labels aus den Features entfernen
    features = features.drop('Result', axis = 1)
    # Liste der Features aus den Namen der Spalten machen
    feature_list = list(features.columns)
    # Features zu einem Array machen
    features = np.array(features)
    return [features, labels]

def train_and_predict(features, labels):
    # Daten in Traings- und Testdaten unterteilen
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)
    
    # Modell instanziieren
    classifier = RandomForestClassifier(n_estimators = 1000, random_state = 42)
    # Trainieren
    classifier.fit(train_features, train_labels)

    # Testen
    predictions = classifier.predict(test_features)
    
    # Wahrheitsmatrix erstellen
    confusion_matrix = metrics.confusion_matrix(test_labels, predictions)

    data = [confusion_matrix, predictions, test_labels]
    return data


for trainingdata_file in data_files:
    csv_data = read_data(trainingdata_file)
    data = train_and_predict()


csv_data = read_data('trainingdata.csv')
data = train_and_predict('rf', csv_data[0], csv_data[1])
accuracy = metrics.accuracy_score(data[4], data[3])
print('Accuracy: ', str(accuracy), '%')

















"""
# Plotting
print(rf_confusion_matrix)
rf_recall = rf_confusion_matrix[0][0] / (rf_confusion_matrix[0][0] + rf_confusion_matrix[1][0])
print(rf_recall)
x = ['Random Forest', 'Logistic Regression']
y_precision = [0.97, 0.92]
plt.bar(x, y_precision, width=0.8, align='center')
plt.xlabel('Algorithm used')
plt.ylabel('Precision')

# plt.show()
"""