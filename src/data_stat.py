#Produces results of statistical analysis of data
import matplotlib.pylab as plt
import numpy as np
import time
import csv 
from ML_Package import *
from operator import itemgetter
from sets import Set 
from libBase import get_config_file_path, get_relation_dir



__author__ = "Haoran Fei <hfei@andrew.cmu.edu>"

#This script takes in the data from CMB in csv format, and draw
#a transaction relationship graph using networkx


def parseCSVstring(string): 
	list = []
	start = 0
	for i in range(len(string)):
		if string[i] == ',':
			list.append(string[start:i])
			start = i+1
	list.append(string[start:len(string)])
	return list

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

#Returns whether the parsed_csv messasge belong to account_name
#if account_name is empty string, then always return true
def filteraccount(parsed_csv, account_name):
	if account_name == "":
		return True
	elif parsed_csv[1] == account_name:
		return True
	else:
		return False


#Start calculating runtime
start_time = time.time()


#File Configs and Global Settings
sample_size = 3000000

path = get_config_file_path("total_data.csv", "data")
#print(path)
csvfile = open(path)
reader = csv.reader(csvfile, delimiter = " ")


data = []

account = "5146C761F90BC0B17307EC91B47BE4AAKP2017082300"

counter = 0
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
	#data.append(completeCSV)
	if filteraccount(completeCSV, account):
		data.append(completeCSV)

data = take_columns(data, [3, 12, 21, 22, 25])
normal_count = 0
anomaly_count = 0

def is_normal(amount, balance):
	if amount < 0 and abs(balance - 0) <= 0.000000001:
		return True
	elif amount >=0 and abs(balance - amount) <= 0.000000001:
		return True
	else:
		return False


for vector in data:
	amount = float(vector[2])
	balance = float(vector[3])
	if is_normal(amount, balance):
		normal_count += 1
	else:
		anomaly_count += 1

print("The amount of normal transactions is: {}".format(normal_count))
print("The amount of anomalous transactions is: {}".format(anomaly_count))


'''
#Extracting 4 dimensions: account number, group number, transaction amount, account balance and summary code
data = take_columns(data, [3, 12, 21,22, 25])

negative_count = 0
for vector in data:
	if float(vector[3]) < 0:
		negative_count += 1
		print(vector)
		print("\n")

print("the number of accounts with negative balance is: {}".format(negative_count))
'''


'''
counter = 0
is1_counter = 0
not1_counter = 0
for vector in data:
	if vector[4] == "NNNN":
		print(vector)
		counter += 1
		if vector[2] == "1.0" or vector[2] == "-1.0":
			is1_counter += 1
		else:
			not1_counter += 1

print("Total number of transactions with summary code NNNN is: {}".format(counter))
print("Total number of transactions with summary code NNNN and transaction amount +-1 is: {}".format(is1_counter))
print("Total number of transactions with summary code NNNN and transaction amount not 1 is: {}".format(not1_counter))
'''


