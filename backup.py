#!/usr/bin/python

import os, re
from os import path
from datetime import datetime

#Change vars, if you use another paths
#If you put config to another dir, change var 'config' in all scripts
#All scripts (except this) must be in a same dir for correct work

path = '/home/user/' #default path to your scripts    don't forget about '/' in the end 
config = '/home/user/backup.conf'
script_list = ['fullbackup.py', 'diffbackup.py', 'backup.conf', 'recovery.py', 'check.py'] #Names of scripts


def start():
	
        #Log block
        log = parsefile("^logfile:.*", config)
        if log == None:
                print('There is an error with logfile! Check your backup.conf. Using default: /var/log/backup.log')
                log = '/var/log/backup.log'
                if os.path.exists(log)==False:
                        os.system('touch %s' % log)
        else:
                log = log.split(':')
                log = log[1]
        message = 'Starting backup service... '
        writemessage(log, message)

	
	#Checking for scripts existing
	for scrname in script_list:
		if os.path.exists(path + scrname) == False:
			message = 'Cannot find a script: ' + path + scrname + ' Stop working...'
			return writemessage(log, message)	
		message = scrname + '         FOUND'
	
	message = 'All scripts has been found'
	writemessage(log, message)

	if parsefile(path+'fullbackup.py', '/etc/crontab') == None:
		time = parsefile('^full:.*', config)
		if time == None:
			message = 'Error with your config in full:'
			return writemessage(log, message)
		time = time.split(":")
		if len(time)!=3:
			message = 'Error with your config in full:'
                        return writemessage(log, message)
		message = 'Add fullbackup script into crontab...'
		writemessage(log, message)
		time = time[2]
		with open('/etc/crontab', 'a') as file:
			file.write(time+ ' root screen -dmS backup '+ path+'fullbackup.py'+' 2>&1\n')
	
	if parsefile(path+'diffbackup.py', '/etc/crontab') == None:
                time = parsefile('^diff:.*', config)
                if time == None:
                        message = 'Error with your config in diff:'
                        return writemessage(log, message)
                time = time.split(":")
                if len(time)!=3:
                        message = 'Error with your config in diff:'
                        return writemessage(log, message)
                message = 'Add diffbackup script into crontab...'
                writemessage(log, message)
                time = time[2]
                with open('/etc/crontab', 'a') as file:
                        file.write(time+ ' root screen -dmS backup '+ path+'diffbackup.py'+' 2>&1\n')


	
def parsefile(str, config):
	with open(config, 'r') as file:
        	comp = file.readlines()
                for line in comp:
                        res = re.search(str,line)
                        if res != None:
                                return res.group()


def writemessage(log, message):
        message = str(datetime.now())+ ": " +  message
        print (message)
        with open(log, 'a') as file:
                file.write(message+'\n')

start()
