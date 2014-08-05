#!/usr/bin/python

import common

recommenderFile = '../play/test-data/codechanges.txt.inferred_ast_operations.recommender'

RANKING_INDEX = 1
TIME_INDEX = 3

header,results = common.readCSV(recommenderFile)
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
print 'Average ranking = ' + str(common.average(rankings))

print 'maximum time = ' + str(maxTime)
time = [float(x) for x in time]
print 'Average time = '+ str(common.average(time))
