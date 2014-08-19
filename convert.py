#!/usr/bin/python

import json
import sys
import os

DELIMITER_SYMBOL = '#'
ESCAPE_SYMNOL = '~'

EVENT_TYPE = 'eventType'
TIMESTAMP = 'timestamp'
ENTITY = 'entityAddress'
TEXT = 'text'
OFFSET = 'offset'
LENGTH = 'len'

TEXT_CHANGE_SYMBOL = 't'
FILE_EDITED_SYMBOL = 'e'

currentFilePath = ''

def encodeFileEdited(filePath):
	return FILE_EDITED_SYMBOL + filePath

def encodeTextChange(object):
	global currentFilePath
	encoded = ''
	if object[ENTITY] != currentFilePath:
		currentFilePath = object[ENTITY]
		encoded = encodeFileEdited(currentFilePath)
	encoded = TEXT_CHANGE_SYMBOL
	encoded = encoded + object[TIMESTAMP] + DELIMITER_SYMBOL
	encoded = encoded + '' + DELIMITER_SYMBOL # the unknwon replaced text
	encoded = encoded + object[TEXT] + DELIMITER_SYMBOL
	encoded = encoded + object[OFFSET] + DELIMITER_SYMBOL
	encoded = encoded + object[LENGTH] + DELIMITER_SYMBOL
	return encoded

def encodeFileOpen(object):
	return ''	

def encodeFileClose(object):
	return ''

def encodeResourceAdded(object):
	return ''

def encodeResourceDeleted(object):
	return ''

typefunctions= {
	'textChange': encodeTextChange,
	'fileOpen': encodeFileOpen,
	'fileClose': encodeFileClose,
	'resourceAdded': encodeResourceAdded,
	'resourceDeleted': encodeResourceDeleted,
}

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

def traverseFiles(folder):
	changed = ''
	files = os.listdir(folder)
	for file in files:
		f = open(folder + "/" + file,'r')
		f.readline() # first empty line
		for line in f:
			line = line.strip('$@$')
			object = json.loads(line,parse_int=(lambda (str): str))
			object = stringifyDictionary(object)
			if object[EVENT_TYPE] in typefunctions:
				changed += (typefunctions[object[EVENT_TYPE]](object))
	return changed

print traverseFiles(sys.argv[1])


