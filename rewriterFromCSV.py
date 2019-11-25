#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
import collections
from display import Display
from vocabulary import *
from flight import Flight


class RewriterFromCSV(object):

    def __init__(self, voc, df, listOfTerms, threshold):
        """
		Translate a dataFile using a given vocabulary
		"""
        self.vocabulary = voc
        self.dataFile = df
        """ Each dictionnary has a key of the following pattern [partition : modality] """
        self.summaryDict = collections.OrderedDict() # dictionnary for general summary of data
        self.summaryFilteredDict = collections.OrderedDict() # dictionnary for general summary of filtered data
        self.correlationDict = collections.OrderedDict() # dictionnary for correlations between modalities and filter condition
        self.threshold = threshold # threshold value for filter
        self.listOfTerms = None # filtering terms
        self.initListOfTerms(listOfTerms)

    def initDictionnary(self):
        """ Inits dictionnaries for general summary of data with all the modalities of the vocabulary (cover each modality equal to 0)"""
        partitions = self.vocabulary.getPartitions()
        for partition in partitions:
            for mod in partition.modalities:
                self.summaryDict[partition.getAttName() + " : " + mod] = 0.0
                self.summaryFilteredDict[partition.getAttName() + " : " + mod] = 0.0

    def displaySummary(self, dictionnary, lineCount):
        """ Converts all covers in dictionnary into percentage """
        for key in self.summaryDict.keys():
            dictionnary[key] = (dictionnary[key] / lineCount) * 100
            #print(str(key)+" => "+str(dictionnary[key])+" %")

    def readAndRewrite(self):
        """ opens data file, read it line by line then computes summary/correlation/atypical terms and displays figures"""
        try:
            with open(self.dataFile, 'r') as source:
                self.initDictionnary()
                lineCount = 0
                filteredData = [] # array of filtered flights
                for line in source:
                    lineCount += 1
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line, self.vocabulary)
                        if self.filter:
                            f.rewrite(self.summaryDict)
                            f.filter(filteredData, self.listOfTerms, self.threshold)
                print("End : Displaying general summary")
                self.displaySummary(self.summaryDict, lineCount)
                print("-------------- End of general summary ---------------")
                if len(filteredData) != 0:
                    print("Beginning summary on filtered data (" + str(len(filteredData)) + " entries)")
                    for data in filteredData:
                        data.rewrite(self.summaryFilteredDict)
                    print("End of summary for filtered data")
                    self.displaySummary(self.summaryFilteredDict, len(filteredData))
                    print("Finding correlations")
                    self.findLinkedTerms()
                    print("Printing correlations with " + str(self.listOfTerms) + " and threshold : " + str(self.threshold))
                    #for key in self.correlationDict.keys():
                        #print(str(key) + " : " + str(self.correlationDict[key]))
                    self.findAtypicalTerms()
                    print("Printing atypical terms with " + str(self.listOfTerms) + " and threshold : " + str(self.threshold))
                    #for term in self.atypicalTermsDict.keys():
                        #print(str(term) + " : " + str(self.atypicalTermsDict[term]))
                    display = Display(self.vocabulary)
                    display.displayPieChartSummary(self.summaryDict, "General Summary for 2008 flights in the USA")
                    display.displayPieChartSummary(self.summaryFilteredDict, "General Summary for 2008 flights with "+str(self.listOfTerms)+" and threshold : " + str(self.threshold))
                    display.displayBubbleChart(self.correlationDict,"Linked terms in 2008 flights with " + str(self.listOfTerms) + " and threshold = " + str(self.threshold))
                    display.displayBubbleChart(self.atypicalTermsDict,"Atypical terms in 2008 flights with " + str(self.listOfTerms) + " and threshold = " + str(self.threshold))
                else:
                    print("Filter returned no entry")
        except:
            raise Exception("Error while loading the dataFile %s" % self.dataFile)

    def initListOfTerms(self, listOfTerms):
        """ Initializes listOfTerms dictionnary, used to filter data """
        if listOfTerms is not None:
            self.listOfTerms = dict()
            self.filter = True
            for element in listOfTerms:
                partition = element.split(':')[0]
                modalities = element.split(':')[1]
                self.listOfTerms[partition] = modalities.split(";")
            print("Filtering flight's list with " + str(self.listOfTerms) + " and threshold : " + str(self.threshold))
        else:
            self.filter = False

    def findLinkedTerms(self):
        """ Computes for each modality of the dictionnary the correlation value between the modality and the filter condition """
        for key in self.summaryDict.keys():  # v' in the formula
            if self.getCoverFromModalityInDictionnary(self.summaryDict, key) == 0:
                correlation = 0
            else:
                dep = self.getCoverFromModalityInDictionnary(self.summaryFilteredDict,key) / self.getCoverFromModalityInDictionnary(self.summaryDict, key) #cover(v',R')/cover(v'R)
                if dep <= 1:
                    correlation = 0
                else:
                    correlation = 1 - (1 / dep)
            self.correlationDict[key] = correlation

    def findAtypicalTerms(self):
        """ Computes for each modality of the dictionnary the atypicity value """
        self.atypicalTermsDict = collections.OrderedDict()
        distanceList = list()
        distance = 0
        for key in self.summaryFilteredDict:
            partitionName = str(key).split(" :")[0]
            partition = voc.getPartition(partitionName)
            modNames = partition.getModNames()
            currentModality = str(key).split(": ")[1]
            indexCurrentModality = modNames.index(currentModality)
            coverCurrentModality = self.getCoverFromModalityInDictionnary(self.summaryFilteredDict,partitionName + " : " + currentModality) #cover(v',R)
            if coverCurrentModality > 0:
                for modality in partition.getModalities():
                    coverModality = self.getCoverFromModalityInDictionnary(self.summaryFilteredDict,partitionName + " : " + modality.getName()) # cover(v,R)
                    if modality.isTrapeziumModality():
                        indexModality = modNames.index(modality.getName())
                        distance = abs(indexCurrentModality - indexModality) / (partition.getNbModalities() - 1) #d(v,v')
                    elif modality.isEnumModality():
                        if (modality.getName() == currentModality):
                            distance = 0
                        else:
                            distance = 1
                    distanceList.append(min(distance, 1 - coverCurrentModality, coverModality)) # min(d(v,v'),cover(v,R),1-cover(v',R))
                self.atypicalTermsDict[partitionName + " : " + currentModality] = max(distanceList) # D(v',R)
                distanceList = list()

    def getCoverFromModalityInDictionnary(self, dictionnary, key):
        """ returns the cover in the dictionnary of the specified modality """
        return dictionnary[key] / 100


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python flight.py <vocfile> <dataFile> <optional><partition1:mod1;mod2...,partition2:mod1;mod2,....> <optional><threshold>")
    else:
        listOfTerms = None
        threshold = None
        if (len(sys.argv) > 3):
            listOfTerms = sys.argv[3].split(",")
            if (len(sys.argv) == 5):
                threshold = float(sys.argv[4])
            else:
                threshold = 0.0
        if os.path.isfile(sys.argv[1]):
            voc = Vocabulary(sys.argv[1])
            if os.path.isfile(sys.argv[2]):
                rw = RewriterFromCSV(voc, sys.argv[2], listOfTerms, threshold)
                rw.readAndRewrite()
            else:
                print("Data file %s not found" % (sys.argv[2]))
        else:
            print("Voc file %s not found" % (sys.argv[2]))
