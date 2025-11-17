# apply_jobs.py - Enhanced job application automation with logging
import time, random, logging, os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger import log_application

# Setup logging
logger = logging.getLogger(__name__)

def random_delay(min_sec, max_sec):
    """Random delay between actions"""
    t = random.uniform(min_sec, max_sec)
    logger.info(f"Waiting {t:.2f} seconds before next action...")
    time.sleep(t)

def apply_to_job(driver, job, config):
    """
    Attempt to apply to a job listing.
    Supports LinkedIn Easy Apply and manual applications.
    """
    job_title = job.get('title', 'Unknown')
    company = job.get('company', 'Unknown')
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Attempting to apply: {job_title} at {company}")
    logger.info(f"Job link: {job.get('link', 'N/A')}")
    logger.info(f"{'='*60}")
    
    try:
        # Navigate to job
        driver.get(job['link'])
        random_delay(*config['delay_range_sec'])
        
        status = apply_to_job_linkedin(driver, job, config)
        
        # Log the application
        log_application(job, status)
        logger.info(f"Application status: {status}\n")
        return status
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error applying to job: {error_msg}")
        log_application(job, 'failed', error=error_msg)
        return 'failed'

def apply_to_job_linkedin(driver, job, config):
    """
    Attempt LinkedIn Easy Apply application.
    """
    try:
        logger.info("Looking for Easy Apply button...")
        
        # Multiple selector strategies for Easy Apply button
        easy_apply_selectors = [
            'button[aria-label*="Easy Apply"]',
            'button:contains("Easy Apply")',
            '[data-test-job-apply-button]',
            'button.jobs-apply-button'
        ]
        
        apply_button = None
        for selector in easy_apply_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    apply_button = elements[0]
                    logger.info(f"Found Easy Apply button with selector: {selector}")
                    break
            except:
                continue
        
        if not apply_button:
            # Try XPath as fallback
            try:
                apply_button = driver.find_element(By.XPATH, '//button[contains(text(), "Easy Apply")]')
                logger.info("Found Easy Apply button using XPath")
            except:
                logger.warning("Easy Apply button not found. This may be a complex application.")
                return 'manual_required'
        
        # Click Easy Apply button
        logger.info("Clicking Easy Apply button...")
        apply_button.click()
        random_delay(*config['delay_range_sec'])
        
        # Handle application form
        logger.info("Processing application form...")
        status = handle_application_form(driver, job, config)
        
        return status
        
    except Exception as e:
        logger.error(f"Error in LinkedIn Easy Apply: {e}")
        return 'failed'

def handle_application_form(driver, job, config):
    """
    Handle the application form after clicking Easy Apply.
    """
    try:
        # Wait for modal/form to appear
        logger.info("Waiting for application form to appear...")
        time.sleep(2)
        
        # Try to find and handle file upload if present
        logger.info("Checking for file upload fields...")
        upload_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
        
        if upload_inputs and config.get('resume_path'):
            if os.path.exists(config['resume_path']):
                logger.info(f"Uploading resume: {config['resume_path']}")
                upload_inputs[0].send_keys(os.path.abspath(config['resume_path']))
                random_delay(*config['delay_range_sec'])
            else:
                logger.warning(f"Resume file not found: {config['resume_path']}")
        
        # Look for submit button
        submit_selectors = [
            'button[aria-label*="Submit"]',
            'button[aria-label*="Finish"]',
            'button:contains("Submit")',
            'button[type="submit"]'
        ]
        
        submit_button = None
        for selector in submit_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    submit_button = elements[0]
                    logger.info(f"Found submit button with selector: {selector}")
                    break
            except:
                continue
        
        if submit_button:
            logger.info("Submitting application...")
            submit_button.click()
            random_delay(3, 5)  # Wait for submission
            logger.info("Application submitted successfully!")
            return 'success'
        else:
            logger.warning("Submit button not found. Manual completion may be required.")
            return 'partial'
    
    except Exception as e:
        logger.error(f"Error handling application form: {e}")
        return 'failed'

def apply_batch_jobs(driver, jobs, config, max_applications=None):
    """
    Apply to multiple jobs with rate limiting.
    """
    logger.info(f"\n{'#'*60}")
    logger.info(f"Starting batch application process")
    logger.info(f"Total jobs to process: {len(jobs)}")
    logger.info(f"{'#'*60}\n")
    
    results = {'success': 0, 'failed': 0, 'manual_required': 0, 'partial': 0}
    
    for idx, job in enumerate(jobs, 1):
        if max_applications and idx > max_applications:
            logger.info(f"Reached max applications limit: {max_applications}")
            break
        
        logger.info(f"\nProcessing job {idx}/{len(jobs)}")
        status = apply_to_job(driver, job, config)
        
        if status in results:
            results[status] += 1
        
        # Longer delay between applications
        if idx < len(jobs):
            delay = random.uniform(10, 20)
            logger.info(f"Waiting {delay:.0f} seconds before next application...")
            time.sleep(delay)
    
    logger.info(f"\n{'='*60}")
    logger.info("Batch application summary:")
    logger.info(f"  Successful: {results['success']}")
    logger.info(f"  Failed: {results['failed']}")
    logger.info(f"  Manual Required: {results['manual_required']}")
    logger.info(f"  Partial: {results['partial']}")
    logger.info(f"{'='*60}\n")
    
    return results
