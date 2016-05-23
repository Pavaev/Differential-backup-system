#!/usr/bin/python
import re, os, subprocess

def check():
	checking = parsefile('full:.*')
	checking = checking.split(":")
	checking = checking[1]

	md5 = os.listdir(checking)
	for i in md5:
		if "md5-" in i:
			md5 = i
	checking = checking+"/"+md5

	p = subprocess.Popen(['md5sum', '-c',checking], stdout=subprocess.PIPE, stderr = open("/var/log/backup.log", 'a'))
	out = p.stdout.read()
	out = out.split('\n')
	print(out)
	copylist = []
	for i in out:
		if re.match('.*FAILED$', i): 
			j = i.split(":")
			copylist.append(j[0])
	print(copylist)
	
def parsefile(str):
        with open("backup.conf", 'r') as file:
                comp = file.readlines()
                for line in comp:
                        res = re.match(str,line)
                        if res != None:
                                return res.group()
	
check()
