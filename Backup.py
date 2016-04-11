#!/usr/bin/env python
import ConfigParser
import os
import time
import datetime
import subprocess
import smtplib 
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

#Read Config of mysql
def config_parser():
  config = ConfigParser.ConfigParser()
  config.read("/etc/mysql/debian.cnf")
  username = config.get('client', 'user')
  password = config.get('client', 'password')
  hostname = config.get('client', 'host')
 
  filestamp = time.strftime('%Y-%m-%d-%I-%M')
 #Mysql Database backup 
  database_list_command="mysql -u %s -p%s -h %s --silent -N -e 'show databases'" % (username, password, hostname)
  for database in os.popen(database_list_command).readlines():
      database = database.strip()
      if database == 'information_schema':
          continue
      if database == 'performance_schema':
          continue
      if database == 'phpmyadmin':
          continue 
      filename = "/root/backup/%s-%s.sql" % (database, filestamp)
      os.popen("mysqldump -u %s -p%s -h %s -e --opt -c %s | gzip -c > %s.gz" % (username, password, hostname, database, filename))
 
#tar to backup /var/www
def www_backup():
  path = "/var/www/"
  for dirnames in os.listdir(path):
   # print dirnames
    filestamp = time.strftime('%Y-%m-%d-%I-%M')
    date = filestamp + "tar.%s.gz" % dirnames
    #print date 
    backup = "/root/backup/%s" % date
    subprocess.Popen(['tar', '-czPf',backup, "/var/www/%s" % dirnames])

# #Delete the old files test
def delete_oldfiles():
  path = "/root/backup/"
  for dirpath, dirnames, filenames in os.walk(path):
    for file in filenames:
      curpath = os.path.join(dirpath, file)
      file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
      if datetime.datetime.now() - file_modified > datetime.timedelta(days=5):
        os.remove(curpath)
  print "delete the old files"

def email_send():
  gmail = ""
  password = ""
  From = ""
  To = [""]
  Sub = 'Sucessful'
  Text= 'Backup Completed Sucessfully'
  message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
              """ % (From, To, Sub, Text)
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.ehlo()
  server.starttls()
  server.login(gmail, password)
  server.sendmail(From, To, message)
  server.close()
  print "mail sent sucessfully"

#call function 
config_parser() 
www_backup()
delete_oldfiles()
email_send()

