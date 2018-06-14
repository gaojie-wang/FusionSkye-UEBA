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
from operator import itemgetter

__author__ = "Haoran Fei <hfei@andrew.cmu.edu>"

#some code written by Su Yumo <suym@buaa.edu.cn>

def parseCSVstring(string): 
	list = []
	start = 0
	for i in range(len(string)):
		if string[i] == ',':
			list.append(string[start:i])
			start = i+1
	list.append(string[start:len(string)])
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

#Take the ith column of data (a list of lists) and return it as a list
def take_column(data, i):
	output = []
	for j in range(len(data)):
		output.append(data[j][i])
	return output

#Take the columns(specified in cols) of data (which is a list of lists)
#Return a list of lists
def take_columns(data, cols):
	output = []
	for row in data:
		newrow = []
		for j in cols:
			newrow.append(row[j]) 
		output.append(newrow)
	return output


#Perform dimensionality reduction
def dim_reduce(data, viz_model, viz_dims):
	if(viz_model == "PCA"):
		data_process = Model_PCA(data, viz_dims)
		data_process = data_process.T
		return data_process
	elif(viz_model == "tSNE"):
		#To be Completed
		#Dummy
		return None

#Visualize a dataset using viz_model for dimensionality reduciton
#Reduce to viz_dims
#Input: data_process is a 2-d array, but it has to be in Transpose!
def visualize(data_process, viz_dims):
	if viz_dims == 2:
		x = data_process[0]
		y = data_process[1]

		#Use mathplotlib to visualize data
		ax = plt.subplot(111)
		ax.scatter(x, y)
	
	elif viz_dims == 3:
		x = data_process[0]
		y = data_process[1]
		z = data_process[2]
	
		#Use mathplotlib to visualize data
		ax = plt.subplot(111, projection='3d')
		ax.scatter(x, y, z)

	plt.show()


#File Configs and Global Settings
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
#"L": Local Outlier Factor
learning_model = "L"

#Visulization model
#"PCA": PCA
#"tSNE": tSNE
viz_model = "PCA"

#visualization dimension
#2 or 3
viz_dims = 2

#the number of highest-ranking anomalies to display
select_num = 15


#All dims of CMB data that are potentially useful
#I have deleted all irrelevant dimensions
#based on information provided by CMB officials
#[3,6,12,13,14,15,16,17,20,21,22,23,24,28,29,30,56,57,59]


for row in reader:
	#parse the csv string to a list of strings
	list1 = parseCSVstring(row[0])
	list2 = parseCSVstring(row[1])

	#we construct completeCSV this way because the csv reader will break
	#up one csv string to 2 strings, and the breaking point is in the middle
	#of a field. Thus, one dimension(i.e. string) will be broken up to 2.
	#We must put them back together
	completeCSV = list1[:-1] 
	completeCSV.append(list1[-1] + " " + list2[0])
	completeCSV += list2[1:]
	
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



itrain = preprocess(training_data)
itest = preprocess(testing_data)


#Use the selected model to do unsupervised ML
#And discover anomalies
if learning_model == "I":
	labels, scores = Model_IsolationForest(itrain)
	print("Learning model selected is Isolation Forest")
elif learning_model == "L":
	labels, scores = Model_LocalOutlierFactor(itrain)
	print("Learning model selected is Local Outlier Factor")


print(scores)


anomaly_data = []
anomaly_score = []
#store the anomalous data
for i in range(len(training_data)):
	if labels[i] == -1:
		anomaly_data.append(training_data[i])
		anomaly_score.append(scores[i])

anomalies = zip(anomaly_data, anomaly_score)

#Take the 2nd and 3rd column of anomaly data
#I.e. the columns without account name
#and transform it to a transposed NumPy array
anomaly_amounts = take_columns(anomaly_data, [1, 2])
anomaly_amounts = np.array(anomaly_amounts)
anomaly_amounts = anomaly_amounts.T
visualize(anomaly_amounts, 2)

select_anomalies = sorted(anomalies, key=itemgetter(1), reverse = True)
select_anomalies = select_anomalies[:select_num]


#print the anomalous data
for data, score in select_anomalies:
	print("Anomalous data: ")
	print(data)
	print(" Score: %.3f" % score + "\n")

#Visualization
reduced = dim_reduce(itrain, viz_model, viz_dims)
visualize(reduced, viz_dims)


#print(filterdimensions([1,2,3,4], [0,2]))
#print(filterdimensions([1,2,3,4], [0,1,3]))















