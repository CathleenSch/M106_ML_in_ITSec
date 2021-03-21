import random

# Datei einlesen
filename = 'trainingdata.csv'
file = open(filename, 'r')
lines = file.readlines()
file.close()

# Header-Zeile wegspeichern, dann aus der Liste entfernen
header = lines[0]
lines.pop(0)

# Liste mischen und Header-Zeile wieder vorne anfuegen
random.shuffle(lines)
lines.insert(0, header)

# gemischte Liste wieder in Datei schreiben
file = open(filename, 'w')
file.writelines(lines)
file.close()
