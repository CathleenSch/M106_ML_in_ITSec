
# phishing-classification.py


# (1) Importieren der Bibliotheken
import numpy as np
from sklearn import tree
from sklearn.metrics import confusion_matrix


def decision_tree_train_and_predict(filename):
    # (2) Trainingsdaten aus CSV laden
    training_data = np.genfromtxt(filename, delimiter =',', dtype=np.int32)

    # (3) Unterteilung in Eingabe - und Ausgabedaten
    inputs = training_data[:,:-1]
    outputs = training_data[:,-1]

    # (4) Unterteilung der Daten in Trainings - und Testdaten
    training_inputs = inputs[:2000]
    training_outputs = outputs[:2000]
    testing_inputs = inputs[2000:]
    testing_outputs = outputs[2000:]

    # (5) Erstellen des Klassifizierungsmodells Entscheidungsbaum
    classifier = tree.DecisionTreeClassifier()

    # (6) Trainieren des Modells
    classifier.fit(training_inputs, training_outputs)

    # (7) Berechnen der Vorhersagen
    predictions = classifier.predict(testing_inputs)

    # (8) Bewertung des Modells ( Genauigkeit )
    cm = confusion_matrix(testing_outputs, predictions)
    data = [cm, predictions, testing_outputs]
    return data
