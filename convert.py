#!/usr/bin/python

import json
import sys
import os

currentFilePath = ''

def encodeTextChange(object):
	pass

def encodeFileOpen(object):
	pass

def encodeFileClose(object):
	pass

def encodeSnapshot(object):
	pass

def encodeResourceAdded(object):
	pass

def encodeResourceDeleted(object):
	pass

typefunctions= {
	'textChange': encodeTextChange,
	'fileOpen': encodeFileOpen,
	'fileClose': encodeFileClose,
	'snapshot': encodeSnapshot,
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
	files = os.listdir(folder)
	for file in files:
		f = open(folder + "/" + file,'r')
		f.readline() # first empty line
		for line in f:
			line = line.strip('$@$')
			object = json.loads(line,parse_int=(lambda (str): str))
			object = stringifyDictionary(object)


traverseFiles(sys.argv[1])


