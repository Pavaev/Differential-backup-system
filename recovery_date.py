#!/usr/bin/python


import re, os, subprocess
from datetime import datetime

def recover():

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
        message = 'Preparing for recover... '
        writemessage(log, message)

	#Find full backup with files.backup and parce it

	message = 'Searching for full backup... '
        writemessage(log, message)

	file_p = parsefile('^full:.*', config)
	file_p = file_p.split(":")
        file_p = file_p[1]
        file_p = file_p+"/fullbackup/files.backup"

	recover = parce_for_recover(file_p)
	if recover == None:
		message = 'There is an error in files.config in full backup'
		return writemessage(log, message)
	if len(recover)==0:
		message = 'files.config in last full backup dir is empty. Nothing to backup'
		writemessage(log, message)
	else:
		message = 'Files from last full backup has been found ' 
		writemessage(log, message)
	
	
		
        message = 'Searching for diff backups... '
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
        temp_bpaths = []
        #Find existing paths
        for bpath in bpaths:
                if os.path.exists(bpath+'/diff') == True:
                        temp_bpaths.append(bpath)

       
        if len(temp_bpaths) == 0:
                message = 'There is no diff backups'
		writemessage(log,message)
        else:   #Else all diff backups by date
                datelist = []
                for temp in temp_bpaths:
                        datelist.append(os.path.getctime(temp))
                datelist.sort(reverse = True)
		print('Type a number to choose a diff backup')	

		diff_choose(datelist)


		lastpath = input()

		if lastpath < 1 and lastpath not in range(1, len(datelist)+1):
			message = 'Error typing!'
			writemessage(log, message)
			raise Exception(message)	
		lastpath = datelist[lastpath-1]
                #Find a path by date
               	for temp in temp_bpaths:
                       	if os.path.getmtime(temp) == lastpath:
                               	lastpath = temp
                               	break
		lastpath = lastpath+"/diff/files.backup"
		message ='Path: '+ lastpath
		writemessage(log, message)
		diff = parce_for_recover(lastpath)
        	if diff == None:
                	message = 'There is an error in files.backup in diff backup'
                	return writemessage(log, message)
        	if len(diff)==0:
                	message = 'files.config in last diff backup dir is empty. Nothing to backup'
                	writemessage(log, message)
        	else:
                	message = 'Files from last diff backup has been found'
                	writemessage(log, message)
		recover.extend(diff)


	if len(recover)==0:
		message = 'Nothing to recover'
		return writemessage(log, message)
	message = 'Starting recover...'
	writemessage(log, message)	
	for cortage in recover:
		print(cortage[0])						
		temp = cortage[0]
		temp = temp.split('/')
		temp.pop()
		temp = '/'.join(temp)
		if os.path.exists(temp)==False:
			subprocess.call(['mkdir', '-p', temp], stderr = open(log, 'a'))
		os.system('rm -rf %s' % cortage[0])		
		subprocess.call(['cp', '-a', cortage[1], cortage[0]], stderr = open(log, 'a'))
		del cortage
	message = 'Recover has been completed successfully'
	writemessage(log,message)


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
		for line in lines:
			a = line.replace("' -> `", " ")
			a = a.replace("`", "")
			a = a.replace("'", "")
			result.append(a.split())
		return result	
		

def diff_choose(datelist):
	 i = 1
         for date_el in datelist:
	         print(str(i)+') '+ str(datetime.fromtimestamp(date_el)))
                 i+=1

	

recover()
