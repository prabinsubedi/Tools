#!/usr/bin/env python
import os 
import datetime 
import time 
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

def email_send(file_arrive):
	fromadd = ""
	toadd = ['','',]  
	msg = MIMEMultipart('alternative')
	part = MIMEApplication(open("/home/wbushby/PaymentFiles/%s" % file_arrive , "rb").read())
	part.add_header('Content-Disposition', 'attachment', filename="%s" % file_arrive) 
	msg.attach(part)
	msg['Subject'] = "Your New File Found"
	msg['From'] = fromadd 
	msg['To'] = ", ".join(toadd)
	text = "Please find the attachment for the new file just arrived"
	part1 = MIMEText(text, 'plain') 
	msg.attach(part1)
#SES configuration	
	smtp_server = 'email-smtp.us-east-1.amazonaws.com'
	smtp_port = '587'
	smtp_do_tls = True 
	smtp_username = ''
	smtp_password = ''
	mail = smtplib.SMTP(
    host = smtp_server,
    port = smtp_port,
    timeout = 10
)
	# mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.set_debuglevel(10)
	mail.ehlo()
	mail.starttls()
	# password = raw_input("Enter Your Email Password")
	mail.login(smtp_username, smtp_password) 
	mail.sendmail(fromadd, toadd, msg.as_string())
	print "mail send with attachment"
	mail.quit()

path = ""
for dirpath, dirnames, filenames in os.walk(path):
	for files in filenames:
		new_path = os.path.join(dirpath, files)
		file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(new_path))
		if datetime.datetime.now() - file_modified < datetime.timedelta(minutes=10):
			#if files.endswith('.CSV'):
			file_arrive = files
			email_send(file_arrive)
print "No file Found"


