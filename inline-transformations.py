#!/usr/bin/python

import csv
import os

transformationFile = '../CodingTracker/postprocessor_root/transformationKinds.csv';
itemSetFolder = '../CodingTracker/postprocessor_root/MiningResults/Frequency';

'''
I read the transformations file and return an a tuple with the \
header and the array of lines (aka transformations).
'''
def readTransformations(file):
	transformations = []
	with open(file,'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		header = reader.next()
		for row in reader:
			transformations.append(row)
	return (header, transformations)

'''
I traverse the folder structure and call the processing function on
each file independently.
'''
def traverseMiningResults(folder, transformations):
	itemSets = os.listdir(folder);
	for itemSet in itemSets:
		processItemSet(folder + "/" + itemSet, transformations);

'''
I do the actual processing of the itemSet* files. I simply inline
the transformation type to make them more human.
'''
def processItemSet(itemSetFile, transformations):
	f = open(itemSetFile,"r");
	output = open(itemSetFile+"-human","w")
	itemSetStr = f.readline()
	descr, items = itemSetStr.split(":", 1)
	items = items[2:len(items) - 2].split(", ")
	output.write(descr+ ": [")
	for item in items:
		index = int(item) - 1
		output.write("("+ transformations[index][1] + ":" + transformations[index][2]+"),")
	output.write("]\n")
	#put the rest of the file in there
	for line in f:
		output.write(line)

header, transformations = readTransformations(transformationFile)
#for i in range(len(transformations)):
#	print(transformations[i][0])
traverseMiningResults(itemSetFolder, transformations)
