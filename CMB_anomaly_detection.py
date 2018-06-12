import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from time import time
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
import csv 


def parseCSVstring(string):
	list = []
	start = 0
	for i in range(len(string)):
		if string[i] == ',':
			list.append(string[start:i])
			start = i+1
	list.append(string[start:i])
	return list


#Dims is a list of integer, representing the 0-indexed indices of dimensions that we think
#are meaningful and worth keeping
def filterdimensions(parsed_csv, dims):
	output = []
	for i in dims:
		output.append(parsed_csv[i])
	return output

training_sample_size = 20000
testing_sample_size = 500

csvfile = open("CMB_1.csv")
reader = csv.reader(csvfile, delimiter = " ")
training_data = []
testing_data = []
counter = 0
dims = [3, 12, 58, 64, 65]

for row in reader:
	completeCSV = parseCSVstring(row[0]) + parseCSVstring(row[1])
	paramlist = filterdimensions(completeCSV, dims)
	if(counter < training_sample_size):
		training_data.append(paramlist)
	else:
		testing_data.append(paramlist)
	counter += 1
	if counter > training_sample_size+ testing_sample_size:
		break

def preprocess(data):
	data = np.array(data)
	label_encoder = LabelEncoder()
	label_encoder.fit(data.flatten())

	integer_encoded = []

	for i in range(len(data)):
		integer_encoded.append(label_encoder.transform(data[i]))

	##onehot_encoded = to_categorical(integer_encoded)

	integer_encoded = np.array(integer_encoded)
	return integer_encoded

itrain = preprocess(training_data)
itest = preprocess(testing_data)

print(itrain[0])

#print(filterdimensions([1,2,3,4], [0,2]))
#print(filterdimensions([1,2,3,4], [0,1,3]))