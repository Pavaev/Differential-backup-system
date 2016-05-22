#!/usr/bin/python
import os,re,subprocess
from datetime import date
def copy():
	filelist = parse("files:.*")
	filelist = filelist[6:]
	week = parse("weekly:.*")
	week = week[7:]
	today = week+'/'+str(date.today())
	filelist = filelist.split()
	week = week.replace(" ", "")
	if os.path.exists(week) == False:
		os.system("mkdir %s" % week)
	else:
		os.system("rm -rf %s/*" % week)
	os.system("touch %s" % today)
	for file in filelist:
		subprocess.call(['cp', '-a', file, week])
		if os.path.isfile(file) == True:
			subprocess.call(['md5sum', file], stdout=open(today, 'a'))	
		else:
			for d, dirs, files in os.walk(file):
				print(file)
				for f in files:
       					path = os.path.join(d,f)
					print(path)
       					subprocess.call(['md5sum', path], stdout=open(today, 'a'))

def parse(str):
	with open("backup.conf", 'r') as file:
		comp = file.readlines()
		for line in comp:
			res = re.match(str,line)
			if res != None:
				return res.group()

copy()
