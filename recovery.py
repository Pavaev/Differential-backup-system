#!/usr/bin/python


import re
from datetime import datetime

def recover():

	config = 'backup.conf'

	 #Log block
        log = parsefile("^logfile:.*", config)
        if log == None:
                print('There is an error with logfile! Check your backup.conf')
        log = log.split(':')
        log = log[1]
        message = 'Preparing for recover... '
        writemessage(log, message)


	file_p = parsefile('^full:.*', config)
	file_p = file_p.split(":")
        file_p = file_p[1]
        file_p = file_p+"/fullbackup/files.backup"

	result = parce_for_recover(file_p)
	print(result)	





def parsefile(str, config):
        with open(config, 'r') as file:
                comp = file.readlines()
                for line in comp:
                        res = re.match(str,line)
                        if res != None:
                                return res.group()


def writemessage(log, message):
        message = str(datetime.now())+ ": " +  message
        print (message)
        with open(log, 'a') as file:
                file.write(message+'\n')


def parce_for_recover(file):
	result = []
	with open(file, 'r') as file:
		lines = file.readlines()
		print (lines)
		for line in lines:
			a = line.replace("' -> `", " ")
			a = a.replace("`", "")
			a = a.replace("'", "")
			print(a)
			result.append(a.split())
		return result	
		


recover()
