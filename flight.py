#!/usr/bin/python
# -*- coding: utf-8 -*-


from vocabulary import Vocabulary
import sys, os


# class used to manage the file airPlane_2008.csv
# Year,Month,DayofMonth,DayOfWeek,DepTime,CRSDepTime,ArrTime,CRSArrTime,UniqueCarrier,FlightNum,TailNum,ActualElapsedTime,CRSElapsedTime,AirTime,ArrDelay,DepDelay,Origin,Dest,Distance,TaxiIn,TaxiOut,Cancelled,CancellationCode,Diverted,CarrierDelay,WeatherDelay,NASDelay,SecurityDelay,LateAircraftDelay
# 2008,1,3,4,2003,1955,2211,2225,WN,335,N712SW,128,150,116,-14,8,IAD,TPA,810,4,8,0,,0,NA,NA,NA,NA,NA
class Flight(object):

    def __init__(self, l, voc):
        """
        Instantiate a Flight from a line of the csv file
        """
        self.vocabulary = voc
        d = l.split(",")
        self.fields = dict()
        try:
            self.fields['DayOfWeek'] = int(d[voc.mapping('DayOfWeek')])
        except:
            self.fields['DayOfWeek'] = None
        try:
            self.fields['DepTime'] = float(int(d[voc.mapping('DepTime')]) / 100) + float(
                int(d[voc.mapping('DepTime')]) % 100) / 100
        except:
            self.fields['DepTime'] = None
        try:
            self.fields['AirTime'] = int(d[voc.mapping('AirTime')])
        except:
            self.fields['AirTime'] = None
        try:
            self.fields['ArrDelay'] = int(d[voc.mapping('ArrDelay')])
        except:
            self.fields['ArrDelay'] = None
        try:
            self.fields['DepDelay'] = int(d[voc.mapping('DepDelay')])
        except:
            self.fields['DepDelay'] = None
        try:
            self.fields['ArrTime'] = int(d[voc.mapping('ArrTime')])
        except:
            self.fields['ArrTime'] = None
        try:
            self.fields['Distance'] = int(d[voc.mapping('Distance')])
        except:
            self.fields['Distance'] = None
        try:
            self.fields['Month'] = d[voc.mapping('Month')]
        except:
            self.fields['Month'] = None
        try:
            self.fields['DayOfMonth'] = int(d[voc.mapping('DayOfMonth')])
        except:
            self.fields['DayOfMonth'] = None
        try:
            self.fields['TaxiIn'] = int(d[voc.mapping('TaxiIn')])
        except:
            self.fields['TaxiIn'] = None
        try:
            self.fields['TaxiOut'] = int(d[voc.mapping('TaxiOut')])
        except:
            self.fields['TaxiOut'] = None
        try:
            self.fields['CarrierDelay'] = int(d[voc.mapping('CarrierDelay')])
        except:
            self.fields['CarrierDelay'] = 0
        try:
            self.fields['WeatherDelay'] = int(d[voc.mapping('WeatherDelay')])
        except:
            self.fields['WeatherDelay'] = 0
        try:
            self.fields['SecurityDelay'] = int(d[voc.mapping('SecurityDelay')])
        except:
            self.fields['SecurityDelay'] = 0
        try:
            self.fields['LateAircraftDelay'] = int(d[voc.mapping('LateAircraftDelay')])
        except:
            self.fields['LateAircraftDelay'] = 0
        try:
            self.fields['Origin'] = d[voc.mapping('Origin')]
        except:
            self.fields['Origin'] = None
        try:
            self.fields['Dest'] = d[voc.mapping('Dest')]
        except:
            self.fields['Dest'] = None

    def __str__(self):
        return "Flight[%s]" % ', '.join(self.fields.values())

    def getValue(self, field):
        ret = None
        if field in self.fields:
            ret = self.fields[field]
        return ret

    def rewrite(self):
        """ Rewrite the flight according to the vocabulary voc (voc is a Vocabulary)"""
        rw = []
        for part in self.vocabulary.getPartitions():
            displayedString = part.getAttName()
            for partelt in part.getModalities():
                val = self.getValue(part.getAttName())
                mu = partelt.getMu(val)
                rw.append(displayedString + " : " + partelt.getName() + "=>" + str(mu))
        return rw

    def rewrite(self, summaryDict):
        """ Rewrite the flight according to the vocabulary voc (voc is a Vocabulary)"""
        for part in self.vocabulary.getPartitions():
            displayedString = part.getAttName()
            for partelt in part.getModalities():
                modality = partelt.getName()
                val = self.getValue(part.getAttName())
                mu = partelt.getMu(val)
                summaryDict[displayedString + " : " + modality] += mu

    def filter(self,filteredData,listOfTerms,threshold):
        for partition in self.vocabulary.getPartitions():
            partitionName = partition.getAttName()
            if partitionName in listOfTerms: #checking if the partition has to be filtered
                for modality in partition.getModalities():
                   if modality.getName() in listOfTerms[partitionName]:  #checking if the modality has to be filtered
                        val = self.getValue(partition.getAttName())
                        mu = modality.getMu(val)
                        if mu > threshold: #checking if modality value in the partition for the flight is > to threshold
                            filteredData.append(self)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python flight.py <vocfile.csv>")
    else:
        if os.path.isfile(sys.argv[1]):
            voc = Vocabulary(sys.argv[1])
            line = "2008,1,3,4,1103,1955,2211,2225,WN,335,N712SW,128,150,116,-14,8,IAD,TPA,810,4,8,0,,0,NA,NA,NA,NA,NA"
            f = Flight(line, voc)
            print(f.rewrite())
