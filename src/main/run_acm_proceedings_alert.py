'''
Run the alert system for WikiCFP.

@author: Yohan
@version: June 21, 2017
'''
import os

email_address = "your@email.address"
alert_interval = 24

os.system("python acm_proceedings_alert.py %s %d" % (email_address, alert_interval))
