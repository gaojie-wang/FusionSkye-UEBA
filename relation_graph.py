import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import time
import csv 
from ML_Package import *
from operator import itemgetter
import networkx as nx
from random import randint
from sets import Set 
import pygraphviz as pgv



__author__ = "Haoran Fei <hfei@andrew.cmu.edu>"

#some code written by Su Yumo <suym@buaa.edu.cn>
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

#Draw a labeled nx graph
def draw_labeled_graph(A, num):	
	#pos=nx.get_node_attributes(G,'pos')
	#pos = nx.circular_layout(G, scale=0.07)

	#plt.figure(num=None, figsize=(11.4, 6.69), dpi=300)

	#Change to pygraphviz graph
	#A = nx.nx_agraph.to_agraph(G)
	

	A.graph_attr['dpi'] = 300
	A.graph_attr['mindist'] = 8
	A.graph_attr['minlen'] = 8

	A.node_attr['color'] = 'red'
	A.node_attr["fixedsize"] = True
	A.node_attr["width"] = 0.25
	A.node_attr["height"] = 0.25
	A.node_attr["fontsize"] = 6

	A.edge_attr['color'] = 'black'
	A.edge_attr['arrow_size'] = 0.5
	A.edge_attr['len'] = 1
	A.edge_attr['labelfontsize'] = 2
	A.layout(prog = 'dot')

	A.draw("relation_graph_{}.png".format(num))

	'''
	pos = graphviz_layout(G, prog='dot')

	nx.draw(G, pos, with_labels=False, node_color='#A0CBE2', width=2)
	
	labels = nx.get_edge_attributes(G,'weight')
	nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
	
	#Figure size equal to the screen size of a 13.3 inch laptop

	
	plt.savefig("relation_graph_{}.png".format(num))
	plt.show()
	'''



#Start calculating runtime
start_time = time.time()


#File Configs and Global Settings
sample_size = 3000000

csvfile = open("total_data.csv")
reader = csv.reader(csvfile, delimiter = " ")

#Largest account is 5146C761F90BC0B17307EC91B47BE4AA

data = []
graph_node = Set()

#Graph data stored as adjacency list, implemented as dict of dicts
graph_dict_by_transaction = {}
graph_dict_by_amount = {}
graph_dict_directed = {}



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
	account = completeCSV[3][-4:]
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
	graph_dict_by_transaction[node] = {}
	graph_dict_by_amount[node] = {}
	graph_dict_directed[node] = {}

for node in graph_node:
	for node2 in graph_node:
		graph_dict_by_transaction[node][node2] = 0
		graph_dict_by_amount[node][node2] = 0
		graph_dict_directed[node][node2] = 0

for group, vectors in grouped_data.iteritems():
	L = len(vectors)
	for i in range(L):
		for j in range(L):
			account1 = vectors[i][0][-4:]
			account2 = vectors[j][0][-4:]
			#Different account, different transaction direction
			if account1 != account2 and vectors[i][1] != vectors[j][1]:
				#increment weight by 1 since weight represents number of transactions
				graph_dict_by_transaction[account1][account2] += 1

				#increment weight by absolute value of transaction amount
				graph_dict_by_amount[account1][account2] += abs(float(vectors[i][2]))
			#Funds flow from account1 to account2
			if account1 != account2 and vectors[i][1] == "D" and vectors[j][1] == "C":
				graph_dict_directed[account1][account2] += 1



#Start creating networkx graph
#G1: only counts number of transaction 
#G2: counts transaction amounts
#G3: only counts number of transactions, but only include edges with >=10 transactions
#G4: only counts number of transactions, but only include edges with >=10 transactions
#G4 is directed. Direction is determined by transaction direction, taking majority vote
#G4's edge weight is percentage of majority direction 
#G5: only counts number of transactions, but only include edges with >=10 transactions
#G5 is directed. Direction is determined by transaction direction, taking majority vote
#G5's edge weight is number of transactions of majority direction
#G6: only counts number of transactions, but only include edges with >=10 transactions
#G6 is directed. Direction is determined by transaction direction, taking majority vote
#G6 has no edge weight

G1 = pgv.AGraph()
G2 = pgv.AGraph()
G3 = pgv.AGraph()
G4 = pgv.AGraph(directed = True)
G5 = pgv.AGraph(directed = True)
G6 = pgv.AGraph(directed = True)

for node in graph_node:
	#rand_pos = (randint(0, len(graph_node)), randint(0, len(graph_node)))
	'''
	G1.add_node(node, pos=rand_pos)
	G2.add_node(node, pos=rand_pos)
	G3.add_node(node, pos=rand_pos)
	G4.add_node(node, pos=rand_pos)
	'''

	G1.add_node(node)
	G2.add_node(node)
	G3.add_node(node)
	G4.add_node(node)
	G5.add_node(node)
	G6.add_node(node)


#Build the first graph
for node1, ndict in graph_dict_by_transaction.iteritems():
	for node2, w in ndict.iteritems():
		#If weight is none-zero
		if w != 0:
			G1.add_edge(node1, node2, label = str(w))

#Build the second graph
for node1, ndict in graph_dict_by_amount.iteritems():
	for node2, w in ndict.iteritems():
		#if weight is non-zero
		if abs(w) >= 0.00000001:
			G2.add_edge(node1, node2, label = str(w))

#Build the third graph
for node1, ndict in graph_dict_by_transaction.iteritems():
	for node2, w in ndict.iteritems():
		#if weight is at least 10
		if w >= 10:
			G3.add_edge(node1, node2, label = str(w))

#Build the fourth graph
for node1, ndict in graph_dict_directed.iteritems():
	for node2, w in ndict.iteritems():
		#get weight of reverse direction
		reverse_w = graph_dict_directed[node2][node1]
		sum_w = w + reverse_w
		if sum_w >= 10:
			if w >= reverse_w:
				#To yield floating point values
				percentage = (w*1.0 /sum_w) * 100
				#Rounding the percentage to 0.01%
				percentage = round(percentage, 2)
				print("Transactions from node1 to node2 is: {}".format(w))
				print("Transactions from node2 to node1 is: {}".format(reverse_w))
				print("Transactions percentage is : {}".format(percentage))
				G4.add_edge(node1, node2, label = str(percentage) + "%")

#Build the fifth graph
for node1, ndict in graph_dict_directed.iteritems():
	for node2, w in ndict.iteritems():
		#get weight of reverse direction
		reverse_w = graph_dict_directed[node2][node1]
		sum_w = w + reverse_w
		if sum_w >= 10:
			if w >= reverse_w:
				G5.add_edge(node1, node2, label = str(w) + "/" + str(reverse_w))

#Build the sixth graph
for node1, ndict in graph_dict_directed.iteritems():
	for node2, w in ndict.iteritems():
		#get weight of reverse direction
		reverse_w = graph_dict_directed[node2][node1]
		sum_w = w + reverse_w
		if sum_w >= 10:
			if w >= reverse_w:
				G6.add_edge(node1, node2)


#Draw both labeled graphs
draw_labeled_graph(G1, 1)
draw_labeled_graph(G2, 2)
draw_labeled_graph(G3, 3)
draw_labeled_graph(G4, 4)
draw_labeled_graph(G5, 5)
draw_labeled_graph(G6, 6)


