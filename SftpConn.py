#!/usr/bin/python

import os
import paramiko
import time 
import datetime 

#Define Server Detail for sftp

server, user, password, port = ('', '', '', 22)
ssh = paramiko.SSHClient()
paramiko.util.log_to_file('paramiko.log')
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect(server, username=user, password=password, port=port)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls /tmp')

error = ssh_stderr.read()

print "err", error, len(error) 

sftp = ssh.open_sftp()
#print "conected"

#The local path where files to be downloded 
local_path = "/root/backup/"  

#The Remote path of the Server 
sftp.chdir(remote_path)
remote_path = '/root/backup/' 

#print "changed"

for filename in (sftp.listdir()):
	
	fullpath = os.path.join(remote_path, filename)
# get timestamp of file in epoch secon
	timestamp  = sftp.stat(fullpath).st_atime  
	createtime = datetime.datetime.now()
	now = time.mktime(createtime.timetuple())
	datetime.timedelta = now - timestamp

#Download the latest file	
	if datetime.timedelta < 86400:
		print filename 

	 	localpath = os.path.join(local_path, filename)
	 	print "downloading %s" % filename
	 	sftp.get(filename, localpath)
	 	print "downloading %s completed" % filename  

sftp.close()
ssh.close()

