
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


def inSum(dict, account):
	sum = 0
	for account1, subdict in dict.iteritems():
		for account2, amount in dict[account1].iteritems():
			if account2 == account:
				sum += dict[account1][account2]
	return sum

def outSum(dict, account):
	sum = 0
	for account2, amount in dict[account].iteritems():
		sum += dict[account][account2]
	return sum 


#Start calculating runtime
start_time = time.time()


#File Configs and Global Settings
sample_size = 3000000

path = get_config_file_path("total_data.csv", "data")
#print(path)
csvfile = open(path)
reader = csv.reader(csvfile, delimiter = " ")

#Largest account is 5146C761F90BC0B17307EC91B47BE4AA

data = []
graph_node = Set()
trans_dict = {}


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
	data.append(completeCSV)

	#add all accounts to graph_node
	account = completeCSV[3]
	if account not in graph_node:
		graph_node.add(account)

	counter += 1
	if counter > sample_size:
		break

#Extracting 4 dimensions: account number, group number, transaction direction and transaction amount
data = take_columns(data, [3, 12, 20, 21])

grouped_data = group_by(data, 1)



#initialize two graph_dicts
for node in graph_node:
	trans_dict[node] = {}

for node in graph_node:
	for node2 in graph_node:
		trans_dict[node][node2] = 0

for group, vectors in grouped_data.iteritems():
	L = len(vectors)
	for i in range(L):
		for j in range(L):
			account1 = vectors[i][0]
			account2 = vectors[j][0]
			#Funds flow from account1 to account2
			if account1 != account2 and vectors[i][1] == "D" and vectors[j][1] == "C":
				trans_dict[account1][account2] += abs(float(vectors[i][2]))

'''
#All 28 accounts:
#02F6FCE4FDC15A6499BB9DDED7C861EC,
#0748E52AB705B4B3D12F057BDEFD898E,
#0DDA75B3AAED571183C62DC7CA00EC48,
#0F60F2F4DE351C11610397AC81581DAE,
#1753FEA4FA8D9F6050022F2B70958CB9,
#1A4057B47BE13A134F47C4932CF3C1E6,
#34E9BDAC6EB44AE32C9EDDFB9463102A,
#3F4F124AB16D622DC694E8C8BE47472B,
#4A0906A4869A1901D6D9F2C239ED8B8C,
#5146C761F90BC0B17307EC91B47BE4AA,
#5B3D2264B7B8F21F5E06F7BBBD6E7A00,
#60B1877042C61E7E046E0F3B5D87C9A4,
#6309E39DD53E3DFB1DAA88425497CC1A,
71E85DC151D764232162F5621868A778,
78D57D726FF0B4F9ADC3B6AACAACBCB2,
8172161393543F94D2BDAF8630CBB080,
8C0D8760B375FB8A314685732B1D32B9,
903FDD52161E3566AC3651CCEEAF864A,
A21890D71BA5CB353ED49996A5662AA6,
B59952EBFECA17E364442EE95C7B2278,
C73F99356848CA08C3979F7DD218211F,
DAB8D4AAD31FE9ED611ACD5EA8FB8DCD,
FA4A94F378190B6C893E5F45095BE29B,
FD1C43BF311AABC8A34E950515EAEE81
'''


#The three internal accounts of first business group
#0748E52AB705B4B3D12F057BDEFD898E
#FA4A94F378190B6C893E5F45095BE29B
#0DDA75B3AAED571183C62DC7CA00EC48

#The three internal accounts of second business group
#0F60F2F4DE351C11610397AC81581DAE
#71E85DC151D764232162F5621868A778
#C73F99356848CA08C3979F7DD218211F

#In this section we focus on analyzing the Second business group
#Source for this group: 8CB9 and 8DCD
#Outlets for this group: (211F out) + (EE81 in) - (211F->EE81)

inflow = inSum(trans_dict, "0F60F2F4DE351C11610397AC81581DAE")
outflow = outSum(trans_dict, "C73F99356848CA08C3979F7DD218211F") + inSum(trans_dict, "FD1C43BF311AABC8A34E950515EAEE81") - trans_dict["C73F99356848CA08C3979F7DD218211F"]["FD1C43BF311AABC8A34E950515EAEE81"]
print("net inflow of this business group is: {}".format(inflow))
print("net outflow of this business group is: {}".format(outflow))




