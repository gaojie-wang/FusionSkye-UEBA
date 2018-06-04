import tensorflow as tf
import time
import numpy as np
import sys
import keras
from keras.models import Sequential
from keras.layers import LeakyReLU
from keras.layers import Dense
from keras.layers import Concatenate

#Hyperparameters
idim = 0


def Encoder(d):
	model = Sequential()
	model.add(LeakyReLU(alpha = 0.1, input_shape = (d,)))
	model.add(Dense(units =32, activation = 'linear'))
	return model

def Generator(d):
	model = Sequential()
	model.add(Dense(units = 64, activation = 'relu', input_dim = 32))
	model.add(Dense(units = 128, activation = 'relu'))
	model.add(Dense(units = d, activation = 'linear'))
	return model

def Discriminator_x(d):
	model = Sequential()
	model.add(Dropout(0.2, input_shape = (d, )))
	model.add(LeakyReLU(alpha = 0.1, input_shape = (d, )))
	return model

def Discriminator_z():
	model = Sequential()
	model.add(Dropout(0.2, input_shape = (32, )))
	model.add(LeakyReLU(alpha = 0.1, input_shape = (32, )))
	return model

def Discriminator(d):
	dx = Discriminator_x(d)
	dz = Discriminator_z()
	combined_tensor = Concatenate([dx, dz])
	combined_tensor.add(Dropout(0.2))
	combined_tensor.add(LeakyReLU(alpha = 0.1))
	combined_tensor.add(Dense(units = 1, activation = 'linear'))


