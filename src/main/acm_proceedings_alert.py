'''
Crawl the proceedings list in the ACM digital library 
and notify if there is any difference.

@author: Yohan
@version: June 25, 2017
'''
import os, urllib2, re, sys, time
from helper import send_email, latest_filepath
from csv_utils import *

email_address = sys.argv[1]
alert_interval = int(sys.argv[2])  # in hour

url = "http://dl.acm.org/proceedings.cfm"
in_dir = "../../ACM"
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
prefix = "ACM Proceedings-"

# Load subscription
proceedings = []
for row in iter_csv_header(in_dir+"/subscription.csv"):
    proceedings.append((row['Conference'], row['Heading']))


while 1:
    now = time.strftime("%Y-%m-%d %H-%M-%S")
    old_record = dict()
    latest_path = latest_filepath(in_dir, prefix)
    if latest_path is not None:
        for row in iter_csv_header(latest_path):
            old_record[row['Event']] = {"Title": row['Event'],
                                           "URL": row['URL']}

    new_record = dict()
    new_html = urllib2.urlopen(urllib2.Request(
                                url, headers={'User-Agent': user_agent})
                               ).read()

    
    for heading, ul in re.findall("<strong><a[^>]+>(.*?)</a></strong>\\s*<ul>(.*?)</ul>",
                                  new_html, re.DOTALL):
        for conference, regex in proceedings:
            if regex != heading: continue
            for li in re.findall("<li .+?</li>", ul):
                url_suffix = re.search('href="(citation.cfm\\?id=[\\d]+)', li)
                event = re.search('title="([^"]+)"', li).group(1)
                event_url = url.replace("proceedings.cfm", url_suffix.group(1))
                new_record[event] = {"Event": event, "URL": event_url}


    # Print the new record
    header = ["Event", "URL"]         
    with open(in_dir+"/"+prefix+now+".csv", 'w') as f:
        out_csv = csv.writer(f)
        out_csv.writerow(header)
        for event, info in sorted(new_record.iteritems()):
            out_csv.writerow([info[k] for k in header])


    updated_set = dict()
    for event, info in new_record.iteritems():
        if event not in old_record:
            updated_set[event] = info
            
    if len(updated_set) == 0:
        print now, ": ", "No update"
    else:
        print "%s : %s" % \
            (now, ", ".join([event for event in sorted(updated_set.keys())]))
            
        subject = "New ACM Proceedings: %s" % \
                  (", ".join([event for event in sorted(updated_set.keys())]))
        
        message = ""
        for event, info in sorted(updated_set.iteritems()):
            message += "%s: %s\n" % (event, info['URL'])
        
        attachment = in_dir+"/"+prefix+now+".csv"
        #print message
        send_email(email_address, subject, message, attachment)
    time.sleep(alert_interval * 3600)    
