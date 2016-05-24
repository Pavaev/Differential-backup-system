#!/usr/bin/python
import re, os, subprocess
import check
from datetime import datetime, date
from os import path

def backup(): 

	config = 'backup.conf'
        #Log block
        log = parsefile("^logfile:.*", config)
        if log == None:
                print('There is an error with logfile! Check your backup.conf')
        log = log.split(':')
        log = log[1]

	#Checking of list of files to be backuped
	filelist  = check.check()
	if filelist == None:
		message = 'Diff backup failed due to previous errors.'
		return writemessage(log, message)
	print(len(filelist))
	if len(filelist)==0:
		message = 'There is no new or modified files for diff backup'
#		return writemessage(log, message)
	

	#If everything is correct, start backup
	message = 'Preparing for diff backup... '
        writemessage(log, message)

	#Find paths for diff backup
	bpaths = parsefile("^diff:.*", config)

	if bpaths == None:
		message = 'There is error in your backup.conf with diff:'
		return writemessage(log, message) 
	bpaths = bpaths.split(":")
	bpaths = bpaths[1]
	bpaths = bpaths.split()
	

	#Is there existing backup dirs
	lastpath = ''
	if os.path.exists(os.getcwd()+'/lastdiff.log'):
		with open('lastdiff.log', 'r') as file:
			lastpath = file.readlines()
		print (lastpath)
		if len(lastpath)!=0 and os.path.exists(os.getcwd()+'/'+lastpath.pop()):
			lastpath = lastpath.pop()
			
		else:
			 lastpath = bpaths[0]
	else: 
		lastpath = bpaths[0]				
		subprocess.call(['mkdir', '-p', 'lastdiff.log'], stderr = open(log, 'a'))		
	print lastpath	
			

  #Make md5 file
        today = lastpath+"/diff/md5-"+str(date.today())


        #Remove files from backup dir
        if os.path.exists(lastpath+'/diff') == False:
                message = 'Make a new dir for full backup. Path: ' + lastpath+'/diff'
                writemessage(log, message)
                subprocess.call(["mkdir", "-p", lastpath+'/diff'], stderr = open(log, 'a'))
        else:
                message = 'Remove old data from backup dir...'
                writemessage(log, message)
                subprocess.call(["rm", '-rf', lastpath,'/diff/*'], stderr = open(log, 'a'))
        os.system("touch %s" % today)

 #Copy and put data into md5 file
        for file in filelist:
                message = 'Starting full backup...'
                writemessage(log,message)
                subprocess.call(['cp', '-a', file, lastpath+'/diff'], stderr = open(log, 'a'))
                message = 'Making md5 file...'
                writemessage(log, message)
                if os.path.isfile(file) == True:
                        print('File:' + file)
                        subprocess.call(['md5sum', file], stdout=open(today, 'a'), stderr = open(log, 'a'))
                else:
                        for d, dirs, files in os.walk(file):
                                for f in files:
                                        path = os.path.join(d,f)
                                        print(path)
                                        print('Path: ' + path)
					subprocess.call(['md5sum', path], stdout=open(today, 'a'), stderr=open(log, 'a'))





        message = 'Diff backup completed'
	writemessage(log, message)
		



def writemessage(log, message):
        message = str(datetime.now())+ ": " +  message
        print (message)
        with open(log, 'a') as file:
                file.write(message+'\n')

def parsefile(str, parsefile):
        with open(parsefile, 'r') as file:
                comp = file.readlines()
                for line in comp:
                        res = re.match(str,line)
                        if res != None:
                                return res.group()




backup()
