#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
from vocabulary import *
from flight import Flight


class RewriterFromCSV(object):

	def __init__(self, voc, df, listOfTerms, threshold):
		"""
		Translate a dataFile using a given vocabulary
		"""
		self.vocabulary = voc
		self.dataFile = df
		self.summaryDict = dict()
		self.listOfTerms = listOfTerms
		self.threshold = threshold


	def initDictionnary(self):
		if self.listOfTerms is None:
			partitions = self.vocabulary.getPartitions()
			for partition in partitions:
				for mod in partition.modalities:
					self.summaryDict[partition.getAttName()+" : "+mod] = 0.0
		else:
			partitions = self.vocabulary.getPartitions()
			for partition in partitions:
				for mod in partition.modalities:
					if mod in listOfTerms:
						self.summaryDict[partition.getAttName()+" : "+mod] = 0.0

	def displaySummary(self,lineCount):
		for key in self.summaryDict.keys():
			self.summaryDict[key] = (self.summaryDict[key]/lineCount)*100
			print(key+" => ", self.summaryDict[key], "%")

	def readAndRewrite(self):
		try:
			with open(self.dataFile, 'r') as source:
				self.initDictionnary()
				print(self.summaryDict)
				lineCount = 0
				for line in source:
					lineCount += 1
					line = line.strip()
					if line != "" and line[0] != "#":
						f = Flight(line, self.vocabulary)
						if self.listOfTerms is not None:
							f.rewriteWithThreshold(self.summaryDict, self.listOfTerms,self.threshold)
						else:
							f.rewrite(self.summaryDict)
				print("End")
				self.displaySummary(lineCount)
		except:
			raise Exception("Error while loading the dataFile %s" % self.dataFile)


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: python flight.py <vocfile> <dataFile> <optional><term1,term2,....> <optional><threshold>")
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
