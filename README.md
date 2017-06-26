# PaperAlerts

Send alert emails for updates in WikiCFP or ACM Proceedings.

## WikiCFP
 Read [WikiCFP](http://www.wikicfp.org) and send alert emails when a new call-for-papers is available for user-selected conferences.
 * Make `subscription.csv` under `/WikiCFP/` with the columns:
   * `Conference`: The conference name for your reference.
   * `URL`: The URL of the conference series. This URL usually begins with `http://www.wikicfp.com/cfp/program?id=`.
 * Run `python /src/main/wikicfp_alert.py [YOUR_EMAIL_ADDRESS] [UPDATE_INTERVAL]`
   * `[YOUR_EMAIL_ADDRESS]`: Your email address.
   * `[UPDATE_INTERVAL]`: Update interval in hour.
 * Alternatively, change `/src/main/run_wikicfp_alert.py` and run this file.

## ACM Proceedings
 Read [ACM Digital Library](http://dl.acm.org) and send alert emails when new proceedings are available for user-selected conferences.
 * Make `subscription.csv` under `/ACM/` with the columns:
   * `Conference`: The conference name for your reference.
   * `Heading`: The heading of the conference series. The heading appears above the list of the proceedings on [webpage](http://dl.acm.org/proceedings.cfm). 
 * Run `python /src/main/acm_proceedings_alert.py [YOUR_EMAIL_ADDRESS] [UPDATE_INTERVAL]`
   * `[YOUR_EMAIL_ADDRESS]`: Your email address.
   * `[UPDATE_INTERVAL]`: Update interval in hour.
 * Alternatively, change `/src/main/run_acm_proceedings_alert.py` and run this file.

