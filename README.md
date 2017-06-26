# PaperAlerts

Send alert emails for updates in WikiCFP or ACM Proceedings.

## WikiCFP
 * Make `subscription.csv` under `/WikiCFP`.
 ** `Conference`: The conference name for your reference.
 ** `URL`: The URL of the conference series. This URL usually begins with `http://www.wikicfp.com/cfp/program?id=`.
 * Run `python /src/main/wikicfp_alert.py [YOUR_EMAIL_ADDRESS] [UPDATE_INTERVAL]`
 ** `[YOUR_EMAIL_ADDRESS]`: Your email address.
 ** `[UPDATE_INTERVAL]`: Update interval in hour.
 * Alternatively, change `/src/main/run_wikicfp_alert.py` and run this file.

