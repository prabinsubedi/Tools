#!/usr/bin/python

import os
import paramiko
import time 
import datetime 
import smtplib 
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP


#Define Server Detail

server, user, password, port = ('', 'root', '', 22)
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

local_path = "/root/backup/"

remote_path = '/root/backup/'
sftp.chdir(remote_path)
print "changed"
for filename in (sftp.listdir()):
	
	fullpath = os.path.join(remote_path, filename)
	
	timestamp  = sftp.stat(fullpath).st_atime  # get timestamp of file in epoch secon
	createtime = datetime.datetime.now()
	now = time.mktime(createtime.timetuple())
	datetime.timedelta = now - timestamp
	
	if datetime.timedelta < 86400:
		print filename 

	 	localpath = os.path.join(local_path, filename)
	 	print "downloading %s" % filename
	 	sftp.get(filename, localpath)
	 	print "downloading %s completed" % filename  

sftp.close()
ssh.close()

