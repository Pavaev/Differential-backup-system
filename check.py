#!/usr/bin/python
import re, os, subprocess
from datetime import datetime

def check():

	#Log block
	log = parsefile("^logfile:.*", 'backup.conf')
	if log == None:
		print('There is an error with logfile! Check your backup.conf')
        log = log.split(':')
        log = log[1]
        message = 'Starting checking at: '
        message = message + str(datetime.now())
        print (message)
        with open(log, 'a') as file:
                file.write(message+'\n')
	pattern = '.*FAILED$'		
	copylist = modified_deleted(log,pattern)
	if copylist == None:
		with open(log, 'a') as file:
			file.write('Cannot find last backup file. Check you backup.conf\n')
			print('Cannot find last backup file. Check you backup.conf')
		return None	
	
	#Print results of modify checking
	if len(copylist)!=0:
		message = "Modified files:"
		printresults(copylist, log, message)
	else:
		print('There is no modified files\n')

	#Print results of remove checking
	pattern = '.*FAILED .*'
	removedlist = modified_deleted(log, pattern)
	if len(removedlist)!=0:
                message = "Removed files:"
                printresults(removedlist, log, message)
        else:
                print('There is no removed files\n')
					
	newlist = newfiles(log)

	#Print results of new files
	if len(newlist)!=0:
                message = "New files:"
                printresults(newlist, log, message)
        else:
                print('There is no new files\n')


def parsefile(str, parsefile):
        with open(parsefile, 'r') as file:
                comp = file.readlines()
                for line in comp:
                        res = re.match(str,line)
                        if res != None:
				return res.group()
				
				
def modified_deleted(log, pattern):
        checking = findmd5()
	
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


def newfiles(log):
	newlist = []
	md5file = findmd5()
	filelist = parsefile("^files:.*", 'backup.conf')
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
def findmd5():
	checking = parsefile('full:.*', 'backup.conf')
        if checking == None:
                print('There is an error with "full:"! Check your backup.conf')
                with open(log, 'a') as file:
                        file.write('There is an error with "full:". Check your backup.conf')
        checking = checking.split(":")
        checking = checking[1]
	if os.path.exists(checking)==False:
		return None
        md5 = os.listdir(checking)
        for i in md5:
                if "md5-" in i:
                        md5 = i
        checking = checking+"/"+md5
	return checking
	
