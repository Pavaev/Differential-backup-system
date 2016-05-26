#!/usr/bin/python
import os,re,subprocess, check
from datetime import date, datetime
def copy():
	
	config = 'backup.conf'

	#Log block
        log = parsefile("^logfile:.*", config)
        if log == None:
        	print('There is an error with logfile! Check your backup.conf. Using default: /var/log/backup.log')
		log = '/var/log/backup.log'
		if os.path.exists(log)==False:
                        os.system('touch %s' % log)

        log = log.split(':')
        log = log[1]
        message = 'Preparing for full backup... '
        writemessage(log, message)

	#Parse config
	filelist = parsefile("files:.*", config)
	filelist = filelist[6:]
	message = 'Files for backup: '
	writemessage(log, message + filelist)
	full = parsefile("full:.*:", config)
        if full == None:
                message = 'There is an error in your backup.conf with full'
                writemessage(log, message)

	full = full.split(":")
	full = full[1]


	full = full+"/fullbackup"	

	message = 'Backup into: '
	writemessage(log, message + full)
	
	#Make md5 file
	today = full+'/'+"md5-"+str(date.today())

	filelist = filelist.split()

	#Remove files from backup dir
	if os.path.exists(full) == False:
		message = 'Make a new dir for full backup. Path: ' + full
		writemessage(log, message)
		subprocess.call(["mkdir", "-p", full], stderr = open(log, 'a'))
	else:
		message = 'Remove old data from backup dir...'
		writemessage(log, message)
		subprocess.call(["rm", '-rf', full,'/*'], stderr = open(log, 'a'))
		subprocess.call(["mkdir", '-p', full], stderr = open(log, 'a'))
	os.system("touch %s" % today)
	os.system("touch %s" % full+'/files.backup')
	#Copy and put data into md5 file
	message = 'Starting full backup...'
        writemessage(log,message)
	for file in filelist:
		p = subprocess.Popen(['cp', '-av', file, full], stderr = open(log, 'a'), stdout = subprocess.PIPE)
		out = p.stdout.read()
		print(out)
		with open(log, 'a') as bckfile:
			bckfile.write(out)
		with open(full+'/files.backup', 'a') as bckfile:
			bckfile.write(out)
		if os.path.isfile(file) == True:
			subprocess.call(['md5sum', file], stdout=open(today, 'a'), stderr = open(log, 'a'))	
		else:
			for d, dirs, files in os.walk(file):
				for f in files:
       					path = os.path.join(d,f)
					
      					subprocess.call(['md5sum', path], stdout=open(today, 'a'), stderr=open(log, 'a'))
	message = 'Full backup completed'
	writemessage(log, message)



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



copy()
