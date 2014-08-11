import csv
import os

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

'''
I do the average of the elements of list. I expect
int or floats. I return a float result, regarless of
the input type.
'''
def average(list):
	return reduce(lambda x, y: x + y, list)/float(len(list))

'''
I remove the last character for a file. Think of
me like a backspace. Quite useful in lot of 
situations
'''
def backspace(file):
	file.seek(-1,os.SEEK_END)
	file.truncate()

