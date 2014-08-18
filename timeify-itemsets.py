#!/usr/bin/python

import common

atomicTransformationsFile = '../play/test+training-data/atomicTransformations.txt'
itemSetFolder = '../play/test+training-data/MiningResults/Size'

TRANS_ID = 0
TIMESTAMP = 2

transformations = {}


(header, atomicTrans) = common.readCSV(atomicTransformationsFile)

for line in atomicTrans:
	transformations[line[TRANS_ID]] = line[TIMESTAMP]

def processItemSetFile(file, t):
	f = open(file,'r')
	output = open(file+'inline','w')
	output = open(file+'-inline','w')
	output.write(f.readline())
	output.write(f.readline())
	output.write(f.readline())
	for line in f:
		line = line.strip('\n')
		tids = line.split(':')
		for tid in tids:
			oneIds = tid.split(',')
			for id in oneIds:
				output.write(transformations[id])
				output.write(',')
			common.backspace(output)
			output.write(':')
		common.backspace(output)
		output.write('\n')
	f.close()
	output.close()

common.traverseMiningResults(itemSetFolder, None, processItemSetFile)
