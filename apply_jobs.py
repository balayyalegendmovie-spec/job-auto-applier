# apply_jobs.py
import time, random
from selenium.webdriver.common.by import By
from logger import log_application

def random_delay(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def apply_to_job(driver, job, config):
    try:
        driver.get(job['link'])
        random_delay(*config['delay_range_sec'])
        # Example: Click 'Easy Apply' (LinkedIn style)
        apply_buttons = driver.find_elements(By.XPATH, '//button[contains(text(), "Easy Apply")]')
        if apply_buttons:
            apply_buttons[0].click()
            random_delay(*config['delay_range_sec'])
            # Upload resume (edit selector as needed)
            upload_input = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
            if upload_input:
                upload_input[0].send_keys(config['resume_path'])
            random_delay(*config['delay_range_sec'])
            status = 'success'
        else:
            status = 'failed'
        log_application(job, status)
        return status
    except Exception as e:
        log_application(job, 'failed', error=str(e))
        return 'failed'
