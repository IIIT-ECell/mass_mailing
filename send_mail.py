from __future__ import print_function
import time
import sys

# Import smtplib for the actual sending function
import smtplib

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
import email.mime.application
import pdb

final_data = []

if len(sys.argv) == 1:
	print ("\nSYNTAX ERROR\nCorrect Syntax: python send_mail.py MAIL_PASSWORD_HERE\n")
	quit()
else:
	psswrd = sys.argv[1]


########################################

# IMPORTANT CONSTANTS

# File with e-mail address of targets
target_csv = 'target.csv'

# Sender E-Mail Address
email_id = 'ecell@iiit.ac.in'

# Enter your name/organisation name for identification
identification = 'E-Cell IIIT Hyderabad'

# Mailing Server
SMTP_server = 'mail.iiit.ac.in'

# Mail's Subject
subject = "You CA code for Megathon"

attachment_path_and_name = ""

########################################

def get_data():
# target.csv contains list of [S.No, Names, Email Addresses]
	with open(target_csv) as f:
		data = f.readlines()
	data = [i.split(',') for i in data]

	fi = []
	for row in data[1:]:
		fi.append({
						'email': row[2],
						'name': row[1].title(),
						'attachment': attachment_path_and_name
					})
	return fi


mail_details = {
		'email' : email_id,
		'identity': identification,
		'password' : psswrd,
		'SMTP-server' : SMTP_server
		}

def SEND_MAIL(name, to_EMAIL, attachment):
	print("SENDING to %s" %(to_EMAIL))
	TO_EMAIL = to_EMAIL

	# Create a text/plain message
	msg = email.mime.Multipart.MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = mail_details['identity'] + " <" + mail_details['email'] + ">"
	msg['To'] = TO_EMAIL
	msg.preamble = 'This is a multi-part message in MIME format.'

	
	# The main body is just another attachment
	with open('salutation.html', 'r') as f:
		salutation = "".join(f.readlines())
	with open('body.html', 'r') as f:
		body = "".join(f.readlines())
	with open('conclusion.html', 'r') as f:
		conclusion = "".join(f.readlines())
	content = salutation.strip() + " " + name.strip() + body.strip() + " " + conclusion.strip()
	body = email.mime.Text.MIMEText(content, 'html')
	msg.attach(body)
	
	# Attachment
	
	# filename=attachment
	# with open("./" + filename) as fp:
	# 	att = email.mime.application.MIMEApplication(fp.read(),_subtype="jpg")
	# att.add_header('Content-Disposition','attachment',filename=filename)
	# msg.attach(att)
	
	# send via Gmail server
	# NOTE: my ISP, Centurylink, seems to be automatically rewriting
	# port 25 packets to be port 587 and it is trashing port 587 packets.
	# So, I use the default port 25, but I authenticate.
	s = smtplib.SMTP(mail_details['SMTP-server'])
	s.starttls()
	s.login(mail_details['email'], mail_details['password'])
	s.sendmail(mail_details['email'], TO_EMAIL, msg.as_string())
	s.quit()


def wait():
	print("\n#########################################################")
	print("#############   SLOW DOWN! Give me a minute.   ###########")
	print("#########################################################\n")
	time.sleep(60)
	return

if __name__=="__main__":

	final_data = get_data()
	for i, data in enumerate(final_data):
		print("%d/%d: "%(i+1, len(final_data)),end="")
		try:
			SEND_MAIL(data['name'], data['email'], data['attachment'])
		except (smtplib.SMTPRecipientsRefused), err:
			wait()
			continue
		if not i%100 and i!=0:
			wait()
		else:
			time.sleep(2)
	print("All Done!")
