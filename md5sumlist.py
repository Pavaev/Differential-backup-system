#!/usr/bin/python

import os, subprocess

home=os.getcwd()
subprocess.call(['sudo', 'cp', '-a', home, '/backup'])
for d, dirs, files in os.walk(home):
	for f in files:
		path = os.path.join(d,f)
		proc = subprocess.call(['md5sum', path], stdout=open('/home/user/md5list', 'a'))

