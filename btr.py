#!/usr/bin/env python3

# File: btr.py
# Description:
# Usage: 

import argparse
import yaml
from platform import system
from sys import exit
from os import listdir
from getpass import getuser

### GLOBAL VARIABLES ###
# template for default paths for browser data for each browser
paths = {
	'Linux':{
		'chrome':{
			'cache': [],
			'cookies': [],
			'history': []
		},
		'firefox':{
			'cache': [],
			'cookies': [],
			'history': []
		}
	},
	'Windows':{
		'chrome':{
			'cache': [],
			'cookies': [],
			'history': []
		},
		'firefox':{
			'cache': [],
			'cookies': [],
			'history': []
		},
		'edge':{
			'cache': [],
			'cookies': [],
			'history': []
		}
	}
}
acceptedBrowsers = ['chrome','firefox','edge']
dumpOptions = ['all','history','cookies','cache']


### Functions ###

# retieves the command line arguments
def getArgs():
	desc = "Detects inconsistencies in browsing data or dumps browsing data"
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('-b','--browser',choices=acceptedBrowsers,dest='browser',
		help="Select a browser to examine")
	parser.add_argument('-d','--dump',choices=dumpOptions,dest='dump',
		help="Dump data in CSV format and quit")
	parser.add_argument('-u','--user',dest='user',
		help="Specifiy a user directory to search, default is current user")
	parser.add_argument('-c','--config',dest='config',
		help="Specify YAML configuration file with paths to files")
	parser.add_argument('-s','--start',dest='start',
		help="Starting time for analysis")
	parser.add_argument('-e','--end',dest='end',
		help="Ending time for analysis")
	return parser.parse_args()


#gets the name of the randomly generated folder for firefox
def getFirefoxChars(user):
	try:
		dirs = listdir('/home/'+user+'/.mozilla/firefox/')
		for directory in dirs:
			if ".default" in directory:
				return directory
		return None
	except:
		return None

# populates the paths dict based on the system type and provided args.
# If no args are supplied, all browser data for all browsers for each user will
# be used.
def getConfig(systemType, configFile, browser, user):
	# check if config file is present
	if configFile:
		# populate paths
		try:
			with open(configFile, 'r') as confStream:
				conf = yaml.load(confStream)
			for browsers, files in conf[systemType].items():
				for f in files:
					if (list(f.values())[0] == 'default' or list(f.values())[0] == ['default']): #TODO why are some elements in a list and others not?
						continue
					paths[systemType][browsers][list(f.keys())[0]] = list(f.values())[0]
		except Exception as e:
			print ("ERROR: Invalid configuration file.\n",e)
			exit()

	# add file paths for all users if not already set in config
	for browsers in paths[systemType].items():
		if browsers[0] == 'chrome':
			if systemType == 'Linux':
				histPath = '/home/'+user+'/.config/google-chrome/Default/History'
				cachePath = '/home/'+user+'/.cache/google-chrome/Default/Cache'
				cookiePath = '/home/'+user+'/.config/google-chrome/Default/Cookies'
			else:
				histPath = 'C:\\Users\\'+user+'\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'
				cachePath = 'C:\\Users\\'+user+'\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache'
				cookiePath = 'C:\\Users\\'+user+'\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies'
			if browsers[1]['history'] == []:
				paths[systemType]['chrome']['history'].append(histPath)
			if browsers[1]['cache'] == []:
				paths[systemType]['chrome']['cache'].append(cachePath)
			if browsers[1]['cookies'] == []:
				paths[systemType]['chrome']['cookies'].append(cookiePath)

		if browsers[0] == 'firefox':
			randchars = getFirefoxChars(user)
			if not randchars:
				print("WARNING: Firefox not found. If it is installed, please specifiy the file locations in the configuration file")
				continue	# firefox not installed or not in default location
			if systemType == 'Linux':
				histPath = '/home/'+user+'/.mozilla/firefox/'+randchars+'/places.sqlite'
				cachePath = '/home/'+user+'/FILL ME IN WHEN YOU FIND THE LOCATION'
				cookiePath = '/home/'+user+'/.mozilla/firefox/'+randchars+'/cookies.sqlite'
			else:
				histPath = 'C:\\Users\\'+user+'\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'
				cachePath = 'C:\\Users\\'+user+'\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache'
				cookiePath = 'C:\\Users\\'+user+'\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies'
			if browsers[1]['history'] == []:
				paths[systemType]['firefox']['history'].append(histPath)
			if browsers[1]['cache'] == []:
				paths[systemType]['firefox']['cache'].append(cachePath)
			if browsers[1]['cookies'] == []:
				paths[systemType]['firefox']['cookies'].append(cookiePath)

		if browsers[0] == 'edge':
			histPath = 'C:\\Users\\'+user+'\\AppData\\Local\\FILL ME IN WHEN YOU FIND LOCATION'
			cachePath = 'C:\\Users\\'+user+'\\AppData\\Local\\FILL ME IN WHEN YOU FIND LOCATION'
			cookiePath = 'C:\\Users\\'+user+'\\AppData\\Local\\FILL ME IN WHEN YOU FIND LOCATION'
			if browsers[1]['history'] == []:
				paths[systemType]['edge']['history'].append(histPath)
			if browsers[1]['cache'] == []:
				paths[systemType]['edge']['cache'].append(cachePath)
			if browsers[1]['cookies'] == []:
				paths[systemType]['edge']['cookies'].append(cookiePath)
	return

def getCache(filename, browser):
	return

def getHistory(filename, browser):
	return

def getCookies(filename, browser):
	return

def printData(data):
	return

if __name__ == '__main__':
	args = getArgs()
	user = args.user
	if not user:
		user = getuser()
	getConfig(system(), args.config, args.browser, user)
	print(yaml.dump(paths))
