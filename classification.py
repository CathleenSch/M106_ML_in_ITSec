import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

# Daten einlesen
features = pd.read_csv('sources/Training_Dataset.csv')
# Labels extrahieren: letzte Spalte 'Result', die bestimmt ob ein Eintrag Phsihing ist oder nicht
labels = np.array(features['Result'])
# Spalte mit den Labels aus den Features entfernen
features = features.drop('Result', axis = 1)
# Liste der Features aus den Namen der Spalten machen
feature_list = list(features.columns)
# Features zu einem Array machen
features = np.array(features)

# Daten in Traings- und Testdaten unterteilen
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)

# Modell instanziieren
rf = RandomForestClassifier(n_estimators = 1000, random_state = 42)
# Trainieren
rf_training_start = time.time()
rf.fit(train_features, train_labels)
rf_training_stop = time.time()
# Testen
rf_pred_start = time.time()
rf_predictions = rf.predict(test_features)
rf_pred_stop = time.time()
# Zeiten berechnen
rf_training_time = rf_training_stop - rf_training_start
rf_pred_time = rf_pred_stop - rf_training_start
# Output
rf_confusion_matrix = metrics.confusion_matrix(test_labels, rf_predictions)
print('Random Forest Classification')
print(f'Training time: {round(rf_training_time, 2)}s')
print(f'Prediction time: {round(rf_pred_time, 2)}s\n')
print(metrics.classification_report(test_labels, rf_predictions))
print('\n\n')

# Modell instanziieren
logreg = LogisticRegression()
# Trainieren
logreg_training_start = time.time()
logreg.fit(train_features, train_labels)
logreg_training_stop = time.time()
# Testen
logreg_pred_start = time.time()
logreg_predictions = logreg.predict(test_features)
logreg_pred_stop = time.time()
# Zeiten berechnen
logreg_training_time = logreg_training_stop - logreg_training_start
logreg_pred_time = logreg_pred_stop - logreg_pred_start
#Output
logreg_confusion_matrix = metrics.confusion_matrix(test_labels, logreg_predictions)
print('Logistic Regression')
print(f'Training time: {round(logreg_training_time, 2)}s')
print(f'Prediction time: {round(logreg_pred_time, 2)}s\n')
print(metrics.classification_report(test_labels, logreg_predictions))
print('\n\n')


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