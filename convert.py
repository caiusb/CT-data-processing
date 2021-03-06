#!/usr/bin/python

import json
import sys
import os
import base64

DELIMITER_SYMBOL = '#'
ESCAPE_SYMBOL = '~'

LINE_BEGIN_SEQUENCE = '$@$';

EVENT_TYPE = 'eventType'
TIMESTAMP = 'timestamp'
ENTITY = 'entityAddress'
TEXT = 'text'
OFFSET = 'offset'
LENGTH = 'len'

KNOWN_TEXT_FILES = ['.txt', '.java', '.xml', '.mf', '.c', '.cpp', '.c', '.h']

TEXT_CHANGE_SYMBOL = 't'
FILE_EDITED_SYMBOL = 'e'
FILE_NEW_SYMBOL = 'f'
FILE_DELETE_SYMBOL = 'N'
FILE_OPEN_SYMBOL = 'f'

currentFilePath = ''

def escapeString(string):
	return string.replace(ESCAPE_SYMBOL,ESCAPE_SYMBOL+ESCAPE_SYMBOL).replace(DELIMITER_SYMBOL,ESCAPE_SYMBOL+DELIMITER_SYMBOL)

def encodeFileEdited(filePath, timestamp):
	return FILE_EDITED_SYMBOL + filePath + DELIMITER_SYMBOL + timestamp + DELIMITER_SYMBOL

def encodeTextChange(object):
	global currentFilePath
	encoded = ''
	if object[ENTITY] != currentFilePath:
		currentFilePath = object[ENTITY]
		encoded += encodeFileEdited(currentFilePath, object[TIMESTAMP])
	encoded += TEXT_CHANGE_SYMBOL
	encoded += '' + DELIMITER_SYMBOL # the unknwon replaced text
	encoded += escapeString(object[TEXT]) + DELIMITER_SYMBOL
	encoded += object[OFFSET] + DELIMITER_SYMBOL
	encoded += object[LENGTH] + DELIMITER_SYMBOL
	encoded += object[TIMESTAMP] + DELIMITER_SYMBOL
	return encoded

def encodeFileOpen(object):
	return ''	

def encodeFileClose(object):
	return ''

def isbase64(filepath):
	for extension in KNOWN_TEXT_FILES:
		if filepath.endswith(extension):
			return False
	return True

def encodeResourceAdded(object):
	encoded = FILE_NEW_SYMBOL
	encoded += object[ENTITY] + DELIMITER_SYMBOL
	if isbase64(object[ENTITY]):
		decoded = base64.b64decode(object[TEXT])
		encoded += escapeString(decoded) + DELIMITER_SYMBOL
	else:
		encoded += escapeString(object[TEXT]) + DELIMITER_SYMBOL
	encoded += object[TIMESTAMP] + DELIMITER_SYMBOL
	return encoded

def encodeResourceDeleted(object):
	encoded = FILE_DELETED_SYMBOL
	encoded += object[ENTITY] + DELIMITER_SYMBOL
	encoded += object[TIMESTAMP] + DELIMITER_SYMBOL
	return encoded

def encodeRefreshFileOperation(object):
	return ''

def encodeFileSaveOperation(object):
	return ''

typefunctions= {
	'textChange': encodeTextChange,
	'fileOpen': encodeFileOpen,
	'fileClose': encodeFileClose,
	'resourceAdded': encodeResourceAdded,
	'resourceDeleted': encodeResourceDeleted,
	'refresh': encodeRefreshFileOperation,
	'fileSave': encodeFileSaveOperation
}

'''
I convert a dictionary from unicode encode to plain ascii.
'''
def stringifyDictionary(d):
	final = {}
	for k,v in d.items():
		newKey = k.encode('utf-8')
		if isinstance(v, unicode):
			final[newKey] = v.encode('utf-8')
		else:
			if isinstance(v, dict):
				final[newKey] = stringifyDictionary(v)
			else:
				final[newKey] = v
	return final

def translateFile(folder, file):
	changed = ''
	f = open(folder + "/" + file,'r')
	f.readline() # first empty line
	for line in f:
		line = line.strip(LINE_BEGIN_SEQUENCE)
		object = json.loads(line, parse_int=(lambda (str): str)) #don't parse int's
		object = stringifyDictionary(object)
		if object[EVENT_TYPE] in typefunctions:
			changed += (typefunctions[object[EVENT_TYPE]](object))
	return changed

def traverseFiles(folder):
	files = os.listdir(folder)
	files.sort(key = lambda x: os.stat(os.path.join(folder, x)).st_mtime)
	for file in files:
		if os.path.isfile(folder + '/' + file):
			print('processing ' + folder + '/' + file  + '...')
			write(folder, translateFile(folder, file))

def write(folder, text):
	outputfile = 'codechanges.txt'
	output = open(folder + "/" + outputfile, 'a')
	output.write(text)

if len(sys.argv) < 2:
	print "Usage: convert.py <folder-with-things>"
else:
	traverseFiles(sys.argv[1])
