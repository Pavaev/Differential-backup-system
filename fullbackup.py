#!/usr/bin/python
import os,re,subprocess
from datetime import date, datetime
def copy():
	
	config = 'backup.conf'

	#Log block
        log = parsefile("^logfile:.*", config)
        if log == None:
                print('There is an error with logfile! Check your backup.conf')
        log = log.split(':')
        log = log[1]
        message = 'Starting full backup... '
        writemessage(log, message)

	#Parse config
	filelist = parsefile("files:.*", config)
	filelist = filelist[6:]
	print (filelist)
	full = parsefile("full:.*:", config)
	full = full.split(":")
	full = full[1]
	print(full)
	today = full+'/'+"md5-"+str(date.today())
	filelist = filelist.split()

	#Remove files from backup dir
	if os.path.exists(full) == False:
		os.system("mkdir %s" % full)
	else:
		os.system("rm -rf %s/*" % full)
	os.system("touch %s" % today)
	#Copy and make md5 file
	for file in filelist:
		subprocess.call(['cp', '-a', file, full], stderr = open(log, 'a'))
		if os.path.isfile(file) == True:
			subprocess.call(['md5sum', file], stdout=open(today, 'a'), stderr = open(log, 'a'))	
		else:
			for d, dirs, files in os.walk(file):
				for f in files:
       					path = os.path.join(d,f)
					print(path)
      					subprocess.call(['md5sum', path], stdout=open(today, 'a'), stderr=open(log, 'a'))
	message = 'Full backup completed'
	writemessage(log, message)



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



copy()
