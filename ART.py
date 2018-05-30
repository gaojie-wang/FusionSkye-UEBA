from __future__ import print_function
from __future__ import division
import tensorflow as tf
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from time import time
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
import sompy
import csv 

#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Adaptive Resonance Theory
# Copyright (C) 2011 Nicolas P. Rougier
#
# Distributed under the terms of the BSD License.
# -----------------------------------------------------------------------------
# Reference: Grossberg, S. (1987)
#            Competitive learning: From interactive activation to
#            adaptive resonance, Cognitive Science, 11, 23-63
#
# Requirements: python 2.5 or above => http://www.python.org 
#               numpy  1.0 or above => http://numpy.scipy.org
# -----------------------------------------------------------------------------


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


class ART:
    ''' ART class
    Usage example:
    --------------
    # Create a ART network with input of size 5 and 20 internal units
    >>> network = ART(5,10,0.5)
    '''

    def __init__(self, n=5, m=10, rho=.5):
        '''
        Create network with specified shape
        Parameters:
        -----------
        n : int
            Size of input
        m : int
            Maximum number of internal units 
        rho : float
            Vigilance parameter
        '''
        # Comparison layer
        self.F1 = np.ones(n)
        # Recognition layer
        self.F2 = np.ones(m)
        # Feed-forward weights
        self.Wf = np.random.random((m,n))
        # Feed-back weights
        self.Wb = np.random.random((n,m))
        # Vigilance
        self.rho = rho
        # Number of active units in F2
        self.active = 0


    def learn_One(self, X):
        ''' Learn X '''

        # Compute F2 output and sort them (I)
        self.F2[...] = np.dot(self.Wf, X)
        I = np.argsort(self.F2[:self.active].ravel())[::-1]

        for i in I:
            # Check if nearest memory is above the vigilance level
            d = (self.Wb[:,i]*X).sum()/X.sum()
            if d >= self.rho:
                # Learn data
                self.Wb[:,i] *= X
                self.Wf[i,:] = self.Wb[:,i]/(0.5+self.Wb[:,i].sum())
                return self.Wb[:,i], i

        # No match found, increase the number of active units
        # and make the newly active unit to learn data
        if self.active < self.F2.size:
            i = self.active
            self.Wb[:,i] *= X
            self.Wf[i,:] = self.Wb[:,i]/(0.5+self.Wb[:,i].sum())
            self.active += 1
            return self.Wb[:,i], i

        return None,None

    def is_anomaly(self, X):
    	self.F2[...] = np.dot(self.Wf, X)
        I = np.argsort(self.F2[:self.active].ravel())[::-1]

        for i in I:
            # Check if nearest memory is above the vigilance level
            d = (self.Wb[:,i]*X).sum()/X.sum()
            if d >= self.rho:
                # Learn data
                self.Wb[:,i] *= X
                self.Wf[i,:] = self.Wb[:,i]/(0.5+self.Wb[:,i].sum())
                return False, i
        return True, -1




ART_net = ART(7, 20, rho = 0.5)

for i in range(len(itrain)):
	ART_net.learn_One(itrain[i])

classes = []
for j in range(len(itest)):
	B, classification = ART_net.is_anomaly(itest[j])
	classes.append(classification)

plt.plot(classes)
plt.show()













