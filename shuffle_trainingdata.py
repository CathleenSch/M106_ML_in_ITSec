import random

filename = 'trainingdata.csv'
file = open(filename, 'r')
lines = file.readlines()
file.close()

header = lines[0]
lines.pop(0)

random.shuffle(lines)
lines.insert(0, header)

file = open(filename, 'w')
file.writelines(lines)
file.close()
