'''
Crawl the proceedings list in the ACM digital library 
and notify if there is any difference.

@author: Yohan
@version: June 21, 2017
'''
import os, urllib2, re, sys, time
from main.helper import send_email
from csv_utils import *

email_address = sys.argv[1]
alert_interval = int(sys.argv[2])  # in hour

url = "http://dl.acm.org/proceedings.cfm"
in_dir = "../../ACM Proceedings"
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'


# Load subscription
proceedings = []
for row in iter_csv_noheader(in_dir+"/subscription.csv"):
    proceedings.append((row[0], row[1]))


while 1:
        now = time.strftime("%Y-%m-%d %H-%M-%S")
        prev_set = set()
        prev_path = in_dir+"/"+sorted(os.listdir(in_dir))[-1]
        prev_html = open(prev_path).read()
        for li in re.findall("<li .+?</li>", prev_html):
            for title, keyword in proceedings:
                if keyword not in li: continue
                url_suffix = re.search('href="(citation.cfm\\?id=[\\d]+)', li)
                title = re.search('title="([^"]+)"', li)
                prev_set.add((title.group(1) if title != None else keyword, 
                              url.replace("proceedings.cfm", url_suffix.group(1))
                              if url_suffix != None else url))

        new_set = set()
        new_html = urllib2.urlopen(urllib2.Request(
                                    url, headers={'User-Agent': user_agent})
                                   ).read()
        for li in re.findall("<li .+?</li>", new_html):
            for title,keyword in proceedings:
                if keyword not in li: continue
                url_suffix = re.search('href="(citation.cfm\\?id=[\\d]+)', li)
                title = re.search('title="([^"]+)"', li)
                new_set.add((title.group(1) if title != None else keyword, 
                             url.replace("proceedings.cfm", url_suffix.group(1))
                             if url_suffix != None else url))

        with open(in_dir+"/"+now+".html", 'w') as out_file:
            out_file.write(new_html)

        updated_set = new_set - prev_set
        if len(updated_set) == 0: print now, ": ", "No update"
        else:
            print "%s : %s" % \
                (now, ", ".join([title for title, url_suffix in updated_set]))
            message = "Subject: New ACM Proceedings: %s\n\n" % \
                (", ".join([title for title,url_suffix in updated_set]))
            for title,url_suffix in updated_set:
                message += "%s: %s\n" % (title, url_suffix)
            send_email(email_address, message)

        time.sleep(alert_interval * 3600)
