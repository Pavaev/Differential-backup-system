#!/usr/bin/python
import os,re,subprocess
from datetime import date
def copy():
	filelist = parse("files:.*")
	filelist = filelist[6:]
	print (filelist)
	full = parse("full:.*:")
	full = full[5:len(full)-1]
	print(full)
	today = full+'/'+str(date.today())
	filelist = filelist.split()
	if os.path.exists(full) == False:
		os.system("mkdir %s" % full)
	else:
		os.system("rm -rf %s/*" % full)
	os.system("touch %s" % today)
	for file in filelist:
		subprocess.call(['cp', '-a', file, full])
		if os.path.isfile(file) == True:
			subprocess.call(['md5sum', file], stdout=open(today, 'a'))	
		else:
			for d, dirs, files in os.walk(file):
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
