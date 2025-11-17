# run.py
from scraper import load_config, login_and_prepare_driver, search_jobs
from apply_jobs import apply_to_job

def main_automation_process():
    config = load_config()
    driver = login_and_prepare_driver(config['job_portal'], config)
    jobs = search_jobs(driver, config)
    for job in jobs:
        status = apply_to_job(driver, job, config)
        print(f"Applied to {job['title']} at {job['company']}: {status}")
    driver.quit()

if __name__ == '__main__':
    main_automation_process()
