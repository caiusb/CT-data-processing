import csv

'''
I read a csv file and return a tuple with the
header and the contents.
'''
def readCSV(file):
	transformations = []
	with open(file,'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		header = reader.next()
		for row in reader:
			transformations.append(row)
	return (header, transformations)

def average(list):
	return reduce(lambda x, y: x + y, list)/len(list)
