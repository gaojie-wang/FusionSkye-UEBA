import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import time
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
import csv 
from operator import itemgetter
from libBase import get_relation_dir, get_config_file_path



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


#Input:
#data is a list of lists
#dim is the dimension of data to group by
#return: a dict of list of lists
def group_by(data, dim):
	dict = {}
	groups = Set()
	for line in data:
		if line[dim] not in groups:
			groups.add(line[dim])
			dict[line[dim]] = [line[:dim] + line[(dim+1):]]
		else:
			dict[line[dim]].append(line[:dim] + line[(dim+1):])
	return dict  