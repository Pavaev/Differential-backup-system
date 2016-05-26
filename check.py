#!/usr/bin/python
import re, os, subprocess
from datetime import datetime

def check():
	config = '/home/user/backup.conf'


	#Log block
	log = parsefile("^logfile:.*", config)
	if log == None:
		print('There is an error with logfile! Check your backup.conf. Using /var/log/backup.log as default')
		log = '/var/log/backup.log'
		if os.path.exists(log)==False:
			os.system('touch %s' % log)
        log = log.split(':')
        log = log[1]
        message = 'Starting checking... '
	writemessage(log, message)

	#Find modified files
	pattern = '.*FAILED$'		
	copylist = modified_deleted(log,pattern, config)

	#In case of error with your config
	if copylist == None:
		message = 'Cannot find last full backup file. Check you backup.conf or make a full backup'
		return writemessage(log, message)
			
	
	#Print results of modify checking
	if len(copylist)!=0:
		message = "Modified files:"
		printresults(copylist, log, message)
	else:
		message = 'There is no modified files'
		writemessage(log,message)

	#Print results of remove checking
	pattern = '.*FAILED .*'
	removedlist = modified_deleted(log, pattern, config)
	if len(removedlist)!=0:
                message = "Removed files:"
                printresults(removedlist, log, message)
        else:
                message = 'There is no removed files'
		writemessage(log,message)
					
	newlist = newfiles(log, config)

	#Print results of new files
	if len(newlist)!=0:
                message = "New files:"
                printresults(newlist, log, message)
        else:
                message = 'There is no new files'
		writemessage(log, message)
	copylist.extend(newlist)

       #Log block
	message = 'Checking completed'
	writemessage(log, message)


	return copylist

def parsefile(str, parsefile):
        with open(parsefile, 'r') as file:
                comp = file.readlines()
                for line in comp:
                        res = re.match(str,line)
                        if res != None:
				return res.group()
				
				
def modified_deleted(log, pattern, config):
        checking = findmd5(config)
	
	if checking==None:
		return None

        p = subprocess.Popen(['md5sum', '-c',checking], stdout=subprocess.PIPE, stderr=open(log, 'a'))
        out = p.stdout.read()
        out = out.split('\n')
        copylist = []
        for i in out:
                if re.match(pattern, i):
                        j = i.split(":")
                        copylist.append(j[0])
       
	return copylist
 
	
def printresults(list, log, message):
        print(message)
        with open(log, 'a') as file:
		file.write(message+'\n')
		for i in list:
			print(i)
			file.write(i)
			if os.path.exists(i):
                        	file.write(str(datetime.fromtimestamp(os.path.getctime(i)))+'\n')
                        	print(str(datetime.fromtimestamp(os.path.getctime(i))))
	print('\n')


def newfiles(log, config):
	newlist = []
	md5file = findmd5(config)
	filelist = parsefile("^files:.*", config)
	filelist = filelist.split(":")
	filelist = filelist[1]
	filelist = filelist.split()
	for file in filelist:
	       	if os.path.isfile(file) == True:
                       	if parse('.*'+file*'$', md5file) == None:
				newlist.append(file)
               	else:
                       	for d, dirs, files in os.walk(file):
                               	for f in files:
                                       	path = os.path.join(d,f)
					if parsefile(".*"+path+"$",md5file) == None:
						newlist.append(path)
                                       	
        return newlist                               		
def findmd5(config):
	checking = parsefile('full:.*', config)
        if checking == None:
                message = 'There is an error with "full:"! Check your backup.conf'
		writemessage(message)
        checking = checking.split(":")
        checking = checking[1] + '/fullbackup'
	if os.path.exists(checking)==False:
		return None
        md5 = os.listdir(checking)
        for i in md5:
                if "md5-" in i:
                        md5 = i
        checking = checking+"/"+md5
	return checking



def writemessage(log, message):
	message = str(datetime.now())+ ": " +  message
        print (message)
        with open(log, 'a') as file:
                file.write(message+'\n')



