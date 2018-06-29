#Produces results of statistical analysis of data
import matplotlib.pylab as plt
import numpy as np
import time
import csv 
import copy
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
sample_size = 10000000

path = get_config_file_path("not_equal_0_and_less_than_9_18.csv", "data")
#print(path)
csvfile = open(path)
reader = csv.reader(csvfile, delimiter = " ")



data = []
graph_node = Set()
trans_dict = {}


account_to_exclude = "FA4A94F378190B6C893E5F45095BE29B"

nexus = "0748E52AB705B4B3D12F057BDEFD898E"

account_to_include = "8C0D8760B375FB8A314685732B1D32B9"

counter = 0
for row in reader:
	if counter == 0:
		counter += 1
		continue
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
	#if filteraccount(completeCSV, account):
	#	data.append(completeCSV)


	counter += 1
	if counter >= sample_size:
		break

#data = take_columns(data, [3, 12, 21, 22, 25])
data = take_columns(data, [3, 12, 20, 21])

grouped_data = group_by(data, 1)

group_stats = copy.deepcopy(grouped_data)

for key, entry in group_stats.iteritems():
	#first number: number of transactions
	#second number: total amount 
	#third number: total amount (take absolute value)
	#third number: average amount(take absolute value)
	group_stats[key] = [0, 0, 0]


group_num = 0
total_trans_num = 0
total_trans_amount = 0

balance = 0
balance_list = []

for group, vectors in grouped_data.iteritems():
	L = len(vectors)
	g_balance = 0
	to_exclude = False
	for i in range(L):
		for j in range(L):
			account1 = vectors[i][0]
			account2 = vectors[j][0]
			#Funds flow from account1 to account2
			if account1 != account2 and vectors[i][1] == "D" and vectors[j][1] == "C":
				group_stats[group][0] += 1
				group_stats[group][1] += float(vectors[i][2])
			if account1 == nexus and account2 == account_to_include and vectors[i][1] == "D" and vectors[j][1] == "C":
				g_balance -= float(vectors[i][2])
			elif account2 == nexus and vectors[i][1] == "D" and vectors[j][1] == "C":
				g_balance += float(vectors[i][2])

			if account1 == account_to_exclude or account2 == account_to_exclude:
				to_exclude = True

	if not to_exclude:
		balance += g_balance
		balance_list.append(balance)
	if to_exclude:
		print(to_exclude)
		print("currently the balance is: {}".format(balance)) 
	
	#Group is meaningful 
	#I.E. contains at least 1 valid transaction
	if group_stats[group][0] != 0:
		group_stats[group][2] = abs(group_stats[group][1]* 1.0)/group_stats[group][0]
		group_stats[group][2] = round(group_stats[group][2], 2)

		group_num += 1
		total_trans_num += group_stats[group][0]
		total_trans_amount += group_stats[group][2]


print("The total balance of account 898E is: {}".format(balance))

plt.plot(balance_list)
plt.show()

'''
total_trans_num = total_trans_num * 1.0 / group_num
total_trans_amount = total_trans_amount * 1.0 / group_num


print("The total number of groups is {}".format(group_num))
print("On average, in each group, the number of transactions is: {}".format(total_trans_num))
print("On average, in each group, the average transaction amount is: {}".format(total_trans_amount))
'''
'''
for group, stats in group_stats.iteritems():
	if stats[0] != 0:
		print("Group name is:" + group)
		print("The number of transactions in this group is: {}".format(stats[0]))
		print("The total amount of funds transferred in this group is: {}".format(stats[1]))
		print("The average amount of funds transferred in this group, taking absolute value, is: {}".format(stats[2]))
		print("\n")
'''




'''
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



counter = 0
isN_counter = 0
notN_counter = 0
for vector in data:
	if vector[2] == "1.0" or vector[2] == "-1.0":
		counter += 1
		if vector[4] == "NNNN":
			isN_counter += 1
		else:
			notN_counter += 1
			print(vector)


'''
print("Total number of transactions with summary code NNNN is: {}".format(counter))
print("Total number of transactions with summary code NNNN and transaction amount +-1 is: {}".format(is1_counter))
print("Total number of transactions with summary code NNNN and transaction amount not 1 is: {}".format(not1_counter))
'''

print("Total number of transactions with amount +-1 is: {}".format(counter))
print("Total number of transactions with transaction amount +-1 and summary code NNNN is: {}".format(isN_counter))
print("Total number of transactions with transaction amount +-1 and summary code not NNNN is: {}".format(notN_counter))

