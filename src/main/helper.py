'''
Helper functions.

@author: Yohan
@version: June 21, 2017
'''
import os

def send_email(address, subject, message, attachment):
    """Sends an email.
    
    Args:
        address: address to which the message is sent.
        message: the subject and content of the message.
                 e.g., "Subject: [SUBJECT]\n\n[CONTENT]\n"
    """                 
#     os.system("printf \"%s\" | sendmail %s" % (message.replace('"', '\"'), address))
    os.system('mail -s %s "%s" %s <<< "%s"' % (subject, attachment, address, message))
    
def latest_filepath(in_dir, prefix):
    """Finds the latest record and returns its path.
    
    Args:
        in_dir: directory where to find the record.
        prefix: the prefix of the record.
    """
    for filename in sorted(os.listdir(in_dir), reverse=True):
        if not filename.startswith(prefix): continue
        return in_dir+"/"+filename
