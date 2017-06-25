'''
Run the alert system for ACM proceedings.

@author: Yohan
@version: June 21, 2017
'''
import os
from main.helper import send_email

email_address = "zukjimote@gmail.com"
alert_interval = 24

send_email(email_address, "Subject: Test alert system\n\nTesting.")
os.system("python acm_proceedings_alert.py %s %d" % (email_address, alert_interval))
