# logger.py
import csv, datetime, os

LOG_FILE = 'application_log.csv'

def log_application(job, status, error=''):
    fieldnames = ['time', 'title', 'company', 'link', 'status', 'error']
    log_entry = {
        "time": datetime.datetime.now().isoformat(),
        "title": job.get('title'),
        "company": job.get('company'),
        "link": job.get('link'),
        "status": status,
        "error": error
    }
    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)
