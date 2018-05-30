import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from time import time
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
import sompy
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

training_sample_size = 20000
testing_sample_size = 500

csvfile = open("sum.csv")
reader = csv.reader(csvfile, delimiter = " ")
training_data = []
testing_data = []
counter = 0


for row in reader:
	paramlist = parseCSVstring(row[0])
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


#mapsize = [50,50]
mapsize = [50, 50]
som = sompy.SOMFactory.build(itrain, mapsize, mask=None, mapshape='planar', lattice='rect', normalization='var', initialization='pca', neighborhood='gaussian', training='batch', name='sompy')  # this will use the default parameters, but i can change the initialization and neighborhood methods
som.train(n_job=1, verbose='info', train_len_factor = 30)  # verbose='debug' will print more, and verbose=None wont print anything
'''
v = sompy.mapview.View2DPacked(50, 50, 'test',text_size=8)
# could be done in a one-liner: sompy.mapview.View2DPacked(300, 300, 'test').show(som)

som.component_names = ['1','2', '3', '4', '5', '6', '7']
v.show(som, what='codebook', which_dim='all', cmap='jet', col_sz=6) #which_dim='all' default


#first you can do clustering. Currently only K-means on top of the trained som
cl = som.cluster(n_clusters = 7)
# print cl
getattr(som, 'cluster_labels')

v.show(som, what='cluster')
'''
h = sompy.hitmap.HitMapView(50, 50, 'hitmap', text_size=16, show_text=True)
h.show(som)

probs = []

for vector in itest:
	matrix = np.array([vector])
	probability = som.predict_probability(matrix, 6, k = 8)
	probs.append(probability[0][0])
print(probs)
plt.plot(probs)
plt.show()






