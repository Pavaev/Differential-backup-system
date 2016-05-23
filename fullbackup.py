#!/usr/bin/python
import os,re,subprocess
from datetime import date, datetime
def copy():

	log = parse("^logfile:.*")
	print(log)
	log = log.split(':')
	log = log[1]
	print(log)
	message = 'Starting full backup at: '
	message = message + str(datetime.now())
	print (message)
	with open(log, 'a') as file:
		file.write(message+'\n')


	filelist = parse("files:.*")
	filelist = filelist[6:]
	print (filelist)
	full = parse("full:.*:")
	full = full.split(":")
	full = full[1]
	print(full)
	today = full+'/'+"md5-"+str(date.today())
	filelist = filelist.split()
	if os.path.exists(full) == False:
		os.system("mkdir %s" % full)
	else:
		os.system("rm -rf %s/*" % full)
	os.system("touch %s" % today)
	for file in filelist:
		subprocess.call(['cp', '-a', file, full])
		if os.path.isfile(file) == True:
			subprocess.call(['md5sum', file], stdout=open(today, 'a'), stderr = open(log, 'a'))	
		else:
			for d, dirs, files in os.walk(file):
				for f in files:
       					path = os.path.join(d,f)
					print(path)
       					subprocess.call(['md5sum', path], stdout=open(today, 'a'), stderr=open(log, 'a'))

def parse(str):
	with open("backup.conf", 'r') as file:
		comp = file.readlines()
		for line in comp:
			res = re.match(str,line)
			if res != None:
				return res.group()

copy()
