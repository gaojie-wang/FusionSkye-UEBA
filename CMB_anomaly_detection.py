import matplotlib.pylab as plt
from matplotlib.font_manager import FontProperties
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
from time import time
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
import csv 
from ML_Package import *

__author__ = "Haoran Fei <hfei@andrew.cmu.edu>"

#some code written by Su Yumo <suym@buaa.edu.cn>

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

#Returns whether the parsed_csv messasge belong to account_name
#if account_name is empty string, then always return true
def filteraccount(parsed_csv, account_name):
	if account_name == "":
		return True
	elif parsed_csv[3] == account_name:
		return True
	else:
		return False

training_sample_size = 20000
testing_sample_size = 500

csvfile = open("CMB_1.csv")
reader = csv.reader(csvfile, delimiter = " ")
training_data = []
testing_data = []
counter = 0

#Hyperparameters
#Largest account is 5146C761F90BC0B17307EC91B47BE4AA
account_name = "5146C761F90BC0B17307EC91B47BE4AA"

dims = [3,21,22]
#Possible learning models:
#"I": isolation forest
#"D": DBSCAN
#"L": Local Outlier Factor
learning_model = "I"
#PCA dimension
#2 or 3
PCA_dims = 2




#All dims of CMB data that are potentially useful
#I have deleted all irrelevant dimensions
#based on information provided by CMB officials
#[3,6,12,13,14,15,16,17,20,21,22,23,24,28,29,30,56,57,59]


for row in reader:
	#parse the csv string to a list of strings
	completeCSV = parseCSVstring(row[0]) + parseCSVstring(row[1])
	
	#filter by account, if applicable
	if filteraccount(completeCSV, account_name):

		#Filter out the dimensions that we are interested in 
		paramlist = filterdimensions(completeCSV, dims)

		#Add to training or testing data
		if(counter < training_sample_size):
			training_data.append(paramlist)
		else:
			testing_data.append(paramlist)
	
	#Increment total counter
	counter += 1

	#Enough samples, stop reading from csv file
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


#Use the selected model to do unsupervised ML
#And discover anomalies
if learning_model == "I":
	labels, scores = Model_IsolationForest(itrain)
elif learning_model == "D":
	labels, scores = Model_DBSCAN(itrain)
#elif learning_model == "L":


if PCA_dims == 2:
	#PCA dimensionality reduction
	itrain_process = Model_PCA(itrain, 2)
	itrain_process = itrain_process.T
	x = itrain_process[0]
	y = itrain_process[1]

	#Use mathplotlib to visualize data
	ax = plt.subplot(111)
	ax.scatter(x, y)

elif PCA_dims == 3:
	#PCA dimensionality reduction
	itrain_process = Model_PCA(itrain, 3)
	itrain_process = itrain_process.T
	x = itrain_process[0]
	y = itrain_process[1]
	z = itrain_process[2]
	
	#Use mathplotlib to visualize data
	ax = plt.subplot(111, projection='3d')
	ax.scatter(x, y, z)

plt.show()

#print(filterdimensions([1,2,3,4], [0,2]))
#print(filterdimensions([1,2,3,4], [0,1,3]))
















