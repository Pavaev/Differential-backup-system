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
                print('There is an error with logfile! Check your backup.conf. Using /var/log/backup.log as default')
		log = 'var/log/backup.log'
		if os.path.exists(log)==False:
                        os.system('touch %s' % log)

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
		return writemessage(log, message)
	

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
	temp_bpaths = []
	lastpath = ''
	newpath = ''
	#Find existing paths
	for bpath in bpaths:
		if os.path.exists(bpath+'/diff') == True:
			temp_bpaths.append(bpath)
	
	#If there is no existing paths, choose first
	if len(temp_bpaths)==0:
		newpath = bpaths[0]
	else:	#Else find last point of diff backup by date
		datelist = []
		for temp in temp_bpaths:
			datelist.append(os.path.getctime(temp))
		datelist.sort(reverse = True)
		lastpath = datelist[0]
		

		#Find a path by date
		for temp in temp_bpaths:
			if os.path.getctime(temp) == lastpath:
				lastpath = temp
				break
		#Find md5 file in last diff backup dir and check for differences		
		md5 = findmd5(lastpath)
		hasnew = False
		with open(md5, 'r') as readfile:
			lines  = readfile.read()
			for file in filelist:
				p = subprocess.Popen(['md5sum', file], stdout=subprocess.PIPE, stderr=open(log, 'a'))
				out = p.stdout.read()
				if re.search(out, lines) == None:
					hasnew = True
					out = out.split()
					out = out[1]
					message = 'A new file from last diff backup has been found: ' + out
					writemessage(log,message)
				
		if hasnew == False:
			message = 'There is no differences between this and last diff backup'
			return writemessage(log, message)
		elif bpaths.index(lastpath)==len(bpaths)-1:
			newpath = bpaths[0]
		else:
			newpath = bpaths[bpaths.index(lastpath)+1]
			
	message = 'Path to backup: ' + newpath
        writemessage(log, message)
				 

  	#Make md5 file
        today = newpath+"/diff/md5-"+str(date.today())


        #Remove files from backup dir
        if os.path.exists(newpath+'/diff') == False:
                message = 'Make a new dir for diff backup. Path: ' + newpath+'/diff'
                writemessage(log, message)
                subprocess.call(["mkdir", "-p", newpath+'/diff'], stderr = open(log, 'a'))
        else:
                message = 'Remove old data from backup dir...'
                writemessage(log, message)
		
                subprocess.call(["rm", '-rf', newpath], stderr = open(log, 'a'))
		subprocess.call(["mkdir", "-p", newpath+'/diff'], stderr = open(log, 'a'))
        os.system("touch %s" % today)
	os.system("touch %s" % newpath+'/diff/files.backup')
 #Copy and put data into md5 file
	message = 'Starting diff backup...'
        writemessage(log,message)

        for file in filelist:
                p = subprocess.Popen(['cp', '-av', file, newpath+'/diff'], stderr = open(log, 'a'), stdout = subprocess.PIPE)
		out = p.stdout.read()
		print(out)
		with open(log, 'a') as bckfile:
                        bckfile.write(out)
                with open(newpath+'/diff/files.backup', 'a') as bckfile:
                        bckfile.write(out)
                if os.path.isfile(file) == True:
                        subprocess.call(['md5sum', file], stdout=open(today, 'a'), stderr = open(log, 'a'))
                else:
                        for d, dirs, files in os.walk(file):
                                for f in files:
                                        path = os.path.join(d,f)
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

def findmd5(path):
        path = path + '/diff'
        md5 = os.listdir(path)
        for i in md5:
                if "md5-" in i:
                        md5 = i
        path = path+"/"+md5
        return path



backup()
