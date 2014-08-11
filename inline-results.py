#!/usr/bin/python

import os
import common

transformationFile = '../play/training-data/transformationKinds.csv';
resultsFile = '../play/test-data/codechanges.txt.inferred_ast_operations.recommender'
humanFile = '../play/test-data/human.txt'

KIND = 1
TYPE = 2

(header, transformation) = common.readCSV(transformationFile)

input = open(resultsFile,'r')
output = open(humanFile,'w')

for line in input:
	if line[0:2] != 'C:':
		output.write(line)
		continue
	line = line[3:]
	bits = line.split(' ', 1)
	completeness = bits[0]
	output.write(completeness)
	candidates = bits[1].split('/')
	output.write('[')
	current_match = candidates[0].strip('[]').split(',')
	for item in current_match:
		output.write('(')
		output.write(transformation[int(item)][KIND])
		output.write(':')
		output.write(transformation[int(item)][TYPE])
		output.write(')')
		output.write(',')
	output.write(']')
	output.write('\n')

