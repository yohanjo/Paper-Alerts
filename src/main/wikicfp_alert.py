'''
Crawl wikicfp 
and notify if there is any difference.

@author: Yohan
@version: June 21, 2017
'''
import os, urllib2, re, sys, time
from helper import send_email, latest_filepath
from csv_utils import *

email_address = sys.argv[1]
alert_interval = int(sys.argv[2])  # in hour

in_dir = "../../WikiCFP"
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
prefix = "WikiCFP-"

# Load subscription
conferences = []
for row in iter_csv_noheader(in_dir+"/subscription.csv"):
    conferences.append((row['Conference'], row['URL']))


while 1:
    now = time.strftime("%Y-%m-%d %H-%M-%S")
    old_record = dict()
    latest_path = latest_filepath(in_dir, prefix)
    if latest_path is not None:
        for row in iter_csv_header(latest_path):
            old_record[row['Conference']] = {"Conference": row['Conference'],
                                           "Event": row['Event'],
                                           "FullName": row['FullName'],
                                           "When": row['When'],
                                           "Where": row['Where'],
                                           "Deadline": row['Deadline'],
                                           "URL": row['URL']}

    new_record = dict()
    for conference, url in conferences:
        html = urllib2.urlopen(urllib2.Request(
                                url, headers={'User-Agent': user_agent})
                              ).read()

        m = re.search('<tr[^>]+><td> Event </td><td> When </td><td> Where </td><td> Deadline</td></tr>\\s*(<tr.*?</tr>)\\s*(<tr.*?</tr>)', html, re.DOTALL)
        m1 = re.search('<td[^>]+><a href="(.*?)">(.*?)</a></td>\\s*<td[^>]+>(.*?)</td></tr>', m.group(1))
        m2 = re.search('<td[^>]+>(.*?)</td>\\s*<td[^>]+>(.*?)</td>\\s*<td[^>]+>(.*?)</td>', m.group(2))
        
        event_url = "http://www.wikicfp.com/" + m1.group(1)
        event = m1.group(2)
        fullname = m1.group(3)
        when = m2.group(1)
        where = m2.group(2)
        deadline = m2.group(3)

        new_record[conference] = {"Conference": conference,
                                  "Event": event,
                                  "FullName": fullname,
                                  "When": when,
                                  "Where": where,
                                  "Deadline": deadline,
                                  "URL": event_url}
                      
    # Print the new record
    header = ["Conference", "Event", "FullName", "When", "Where", "Deadline", "URL"]         
    with open(in_dir+"/"+prefix+now+".csv", 'w') as f:
        out_csv = csv.writer(f)
        out_csv.writerow(header)
        for info in new_record.values():
            out_csv.writerow([info[k] for k in header])

    updated_set = dict()
    for conference, info in new_record.iteritems():
        if conference not in old_record or info['Deadline'] != old_record[conference]['Deadline']:
            updated_set[conference] = info
            
    if len(updated_set) == 0:
        print now, ": ", "No update"
    else:
        print "%s : %s" % \
            (now, ", ".join([info['Event'] for conference, info in updated_set.iteritems()]))
            
        subject = "New WikiCFP: %s" % \
                  (", ".join([info['Event'] for info in updated_set.values()]))
        
        message = ""
        for conference, info in updated_set.iteritems():
            message += info['Event'] + "\n"
            for k in ['FullName', 'When', 'Where', 'Deadline', 'URL']:
                message += "  - %s: %s\n" % (k, info[k])
            message += "\n\n"
        
        attachment = in_dir+"/"+prefix+now+".csv"
#         print message
        send_email(email_address, subject, message, attachment)
    time.sleep(alert_interval * 3600)
