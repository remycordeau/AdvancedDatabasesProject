#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
import collections
from vocabulary import *
from flight import Flight


class RewriterFromCSV(object):

	def __init__(self, voc, df, listOfTerms, threshold):
		"""
		Translate a dataFile using a given vocabulary
		"""
		self.vocabulary = voc
		self.dataFile = df
		self.summaryDict = collections.OrderedDict()
		self.summaryFilteredDict = collections.OrderedDict()
		self.correlationDict = collections.OrderedDict()
		self.threshold = threshold
		self.listOfTerms = None
		self.initListOfTerms(listOfTerms)


	def initDictionnary(self):
		partitions = self.vocabulary.getPartitions()
		for partition in partitions:
			for mod in partition.modalities:
				self.summaryDict[partition.getAttName()+" : "+mod] = 0.0
				self.summaryFilteredDict[partition.getAttName() + " : " + mod] = 0.0

	def displaySummary(self,dictionnary,lineCount):
		for key in self.summaryDict.keys():
			dictionnary[key] = (dictionnary[key]/lineCount)*100
			#print(str(key)+" => "+str(dictionnary[key])+" %")

	def readAndRewrite(self):
		try:
			with open(self.dataFile, 'r') as source:
				self.initDictionnary()
				lineCount = 0
				filteredData = []
				for line in source:
					lineCount += 1
					line = line.strip()
					if line != "" and line[0] != "#":
						f = Flight(line, self.vocabulary)
						if self.filter:
							f.rewrite(self.summaryDict)
							f.filter(filteredData,self.listOfTerms,self.threshold)
				print("End : Displaying general summary")
				self.displaySummary(self.summaryDict,lineCount)
				print("-------------- End of general summary ---------------")
				if len(filteredData) != 0:
					print("Beginning summary on filtered data ("+str(len(filteredData))+" entries)")
					for data in filteredData:
						data.rewrite(self.summaryFilteredDict)
					print("End of summary for filtered data")
					self.displaySummary(self.summaryFilteredDict,len(filteredData))
					print("Finding correlations")
					self.findLinkedTerms()
					for key in self.correlationDict.keys():
						print("Correlations for : "+str(key))
						for modality in self.correlationDict[key]:
							correlationValue = (self.correlationDict[key])[modality]
							print(str(modality)+" : "+str(correlationValue))
				else:
					print("Filter returned no entry")
		except:
			raise Exception("Error while loading the dataFile %s" % self.dataFile)

	def initListOfTerms(self,listOfTerms):
		if listOfTerms is not None:
			self.listOfTerms = dict()
			self.filter = True
			for element in listOfTerms:
				partition = element.split(':')[0]
				modalities = element.split(':')[1]
				self.listOfTerms[partition] = modalities.split(";")
			print("Filtering flight's list with "+str(self.listOfTerms)+" and threshold : "+str(self.threshold))
		else:
			self.filter = False


	def findLinkedTerms(self):
		for partition in self.listOfTerms.keys():
			for filteredModality in self.listOfTerms[partition]: #v in the formula
				modalityValues = collections.OrderedDict()
				for key in self.summaryDict.keys(): # v' in the formula
					#print(str(partition)+" : "+str(filteredModality))
					#print(key)
					if self.getCoverFromModalityInDictionnary(self.summaryDict,key) == 0:
						correlation = 0
					else:
						dep = self.getCoverFromModalityInDictionnary(self.summaryFilteredDict,key)/self.getCoverFromModalityInDictionnary(self.summaryDict,key)
						if dep <= 1:
							correlation = 0
						else:
							correlation = 1 - (1/dep)
					modalityValues[key] = correlation
				self.correlationDict[partition+" : "+filteredModality] = modalityValues

	def getCoverFromModalityInDictionnary(self,dictionnary,key):
		return dictionnary[key]/100

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: python flight.py <vocfile> <dataFile> <optional><partition1:mod1;mod2...,partition2:mod1;mod2,....> <optional><threshold>")
	else:
		listOfTerms = None
		threshold = None
		if(len(sys.argv) > 3):
			listOfTerms = sys.argv[3].split(",")
			if(len(sys.argv) == 5):
				threshold = float(sys.argv[4])
			else:
				threshold = 0.0
		if os.path.isfile(sys.argv[1]):
			voc = Vocabulary(sys.argv[1])
			if os.path.isfile(sys.argv[2]):
				rw = RewriterFromCSV(voc, sys.argv[2],listOfTerms,threshold)
				rw.readAndRewrite()
			else:
				print("Data file %s not found" % (sys.argv[2]))
		else:
			print("Voc file %s not found" % (sys.argv[2]))
