'''
Helper functions.

@author: Yohan
@version: June 21, 2017
'''
from subprocess import Popen, PIPE, STDOUT
import os

def send_email(address, subject, message, attachment):
    """Sends an email.
    
    Args:
        address: address to which the message is sent.
        subject: subject of the email.
        message: body of the email.
        attachment: attachment path.
    """                 
    if len(subject) > 50: subject = subject[:50] + "..."
    p = Popen(['mail', '-s', subject, '-t', address, '-A', attachment], stdin=PIPE)
    p.communicate(input=message)

    
def latest_filepath(in_dir, prefix):
    """Finds the latest record and returns its path.
    
    Args:
        in_dir: directory where to find the record.
        prefix: the prefix of the record.
    """
    for filename in sorted(os.listdir(in_dir), reverse=True):
        if not filename.startswith(prefix): continue
        return in_dir+"/"+filename
