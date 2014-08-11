#!/usr/bin/python

import common

transformationFile = '../play/training-data/transformationKinds.csv';
resultsFile = '../play/test-data/codechanges.txt.inferred_ast_operations.recommender'
humanFile = '../play/test-data/human.txt'

KIND = 1
TYPE = 2

def inlineItem(item,file):
	file.write('(')
	file.write(transformation[int(item)][KIND])
	file.write(':')
	file.write(transformation[int(item)][TYPE])
	file.write(')')
	file.write(',')


(header, transformation) = common.readCSV(transformationFile)

input = open(resultsFile,'r')
output = open(humanFile,'w')

maxItems = 5;
currentItemCount = 0;
for line in input:
	if line == '----\n':
		currentItemCount = 0;
	if line[0:2] != 'C:':
		output.write(line)
		continue
	if currentItemCount >= maxItems:
		continue;
	line = line[2:]
	bits = line.split(' ', 1)
	completeness = bits[0]
	output.write(completeness)
	candidates = bits[1].split('/')
	output.write('[')
	current_match = candidates[0].strip('[]').split(',')
	for item in current_match:
		inlineItem(item,output)
	common.backspace(output)
	output.write(']')
	output.write('/')
	output.write('[')
	items = candidates[1].strip('[]\n').split(',')
	for item in items:
		inlineItem(item,output)
	common.backspace(output)
	output.write(']')
	output.write('\n')
	currentItemCount = currentItemCount + 1
