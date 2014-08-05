#!/usr/bin/python

import csv

recommenderFile = '../play/test-data/codechanges.txt.inferred_ast_operations.recommender'

RANKING_INDEX = 1
TIME_INDEX = 3

def readCSV(file):
	results = []
	with open(file,'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		header = reader.next()
		for row in reader:
			results.append(row)
	return (header,results)

header,results = readCSV(recommenderFile)
nom_rows = len(results)
num_col = len(results[0])

maxRankings = 0
rankings = []
maxTime = 0;
time = []
for line in results:
	if (line[RANKING_INDEX] > maxRankings):
		maxRankings = line[RANKING_INDEX]
	if (line[TIME_INDEX] > maxTime):
		maxTime = line[TIME_INDEX]
	rankings.append(line[RANKING_INDEX])
	time.append(line[TIME_INDEX])

print 'maximum ranking = ' + str(maxRankings)
rankings = [float(x) for x in rankings]
print 'Average ranking = ' + str(reduce(lambda x, y: x + y, rankings)/len(rankings))

print 'maximum time = ' + str(maxTime)
time = [float(x) for x in time]
print 'Average time = '+ str(reduce(lambda x, y: x + y, time)/len(time))
