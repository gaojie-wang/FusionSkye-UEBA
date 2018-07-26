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


class Formula():
	#id : name of formula
	#facts: data fields used by the formula
	#results: name of tags/numericals computed by the formula
	#f: function, takes in a dict of required facts and computes a dict of results
	#is_tag: True if the Formula computes tags, False if the Formula computes numericals
	def __init__(self, id, facts, results, f, is_tag = True):
		self.id = id
		self.facts = facts
		self.results = results
		self.f = f
		self.is_tag = is_tag

class User():
	def __init__(self, u_id, u_context):
		self.id = u_id
		self.context = u_context
		
		self.facts = dict()
		#A Dict of key-value pairs
		#Key: string, represent the data field name
		#Entry: string, represent the data value

		self.tags = dict()
		#A Dict of key-value pairs
		#Key: string, represent the tag name
		#Entry: bool, represent whether the tag is true or false
		
		self.numericals = dict()
		#A Dict of key-value pairs
		#Key: string, represent the attribute name
		#Entry: float, represent the value of the attribute
		
		#A list of formulas
		self.formulas = []
	
	def importFacts(self, fact_dict):
		for field in fact_dict.keys():
			self.facts[field] = fact_dict[field]

	#Add a formula to the collection of formulas
	def addFormula(self, formula):
		self.formulas.append(formula)

	def addLocalTag(self, name, value = False):
		self.tags[name] = value

	def addLocalNumerical(self, name, value = 0.0):
		self.numericals[name] = value


	#Applies all formulas
	#Updates the tags and numericals
	def update(self):
		for formula in self.formulas:
			inputs = dict()
			for data_field in formula.facts:
				inputs[data_field] = self.facts[data_field]
			to_use = formula.f
			results = to_use(inputs)
			
			if formula.is_tag:
				for tag in results.keys():
					self.tags[tag] = results[tag]
			else:
				for numerical in results.keys():
					self.numericals[numerical] = results[numerical]
	

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


def testScript():
	context = UserProfileContext()
	def f1(inputs):
		output = dict()
		output["square"] = float(inputs["score"]) * float(inputs["score"])
		return output

	formula_1 = Formula("squaring", ["score"], ["square"], f1, False)

	user_1 = User("Haoran", context)

	user_1.importFacts({"score": "5.0"})

	user_1.addLocalNumerical("square")

	user_1.addFormula(formula_1)

	user_1.update()

	print(user_1.getNumerical("square"))


testScript()















