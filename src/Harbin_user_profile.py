# -*- coding: utf-8 -*-


import matplotlib.pylab as plt
from matplotlib.font_manager import FontProperties
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
import time
import sys, os 
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
import csv 
from ML_Package import *
from operator import itemgetter
from libBase import get_relation_dir, get_config_file_path


class UserProfileContext():
	def __init__(self):
	
		self.version = 0.0
		
		self.facts = []
		#A list of strings
		#Represent all data taken for each user
		
		self.tags = []
		#A list of strings
		#Represent all tags
	
		self.numericals = []
		#A list of strings
		#Represent all numerical values/approximations

		self.dynamicGroups = []
		#A list of dynamic groups
		#List of strings
		#Considered a tag
	 	#True if the user is a member, false otherwise

		self.staticGroups = []
		#A list of static groups
		#List of strings
		#Considered a tag
		#True if the user is a member, false otherwise



class User():
	def __init__(self, u_id, u_context, u_tagsF, u_numericalsF):
		self.id = u_id
		self.context = u_context
		
		self.facts = Dict()
		#A Dict of key-value pairs
		#Key: string, represent the data field name
		#Entry: string, represent the data value

		self.tags = Dict()
		#A Dict of key-value pairs
		#Key: string, represent the tag name
		#Entry: bool, represent whether the tag is true or false
		
		self.numericals = Dict()
		#A Dict of key-value pairs
		#Key: string, represent the attribute name
		#Entry: float, represent the value of the attribute
		
		self.tagsF = u_tagsF

		#A function that given facts, compute the values of all tags
		
		self.numericalsF = u_numericalsF
		#A function that given facts and tags, compute the values of all numericals
	

		def update(self):
			pass
		#Updates the tags and numericals based on the stored tagsF and numericalsF
	
		def setTags(self, names, values):
		#Names: a list of strings
		#Values: a list of bools, represent the new values of these tags
			if len(values) == 0:
				for name in names:
					self.tags[name] = False 
			else:
				for i in range(len(names)):
					self.tags[names[i]] = values[i]

		def setNumericals(self, names, values):
		#Names: a list of strings
		#Values: a list of floats, represent the new values of these Numerical fields
			if len(values) == 0:
				for name in names:
					self.tags[name] = 0.0 
			else:
				for i in range(len(names)):
					self.tags[names[i]] = values[i]

		def getTag(self, name):
		#Name: string, name of desired tag
		#Return a bool
			return self.tags[name]

		def getNumerical(self, name):
		#Name: string, name of desired attribute
		#Return a float
			return self.numericals[name]















