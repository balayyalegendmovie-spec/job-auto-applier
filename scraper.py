# scraper.py - Enhanced job scraper with detailed logging
import time, random, json, os, logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('job_scraper.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def random_delay(min_sec, max_sec):
    """Random delay between actions to avoid bot detection"""
    t = random.uniform(min_sec, max_sec)
    logger.info(f"Waiting {t:.2f} seconds...")
    time.sleep(t)

def load_config(config_path='config.json'):
    """Load configuration from JSON file"""
    if not os.path.exists(config_path):
        logger.error(f"Config file {config_path} not found")
        raise FileNotFoundError(f"{config_path} not found")
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            logger.info(f"Configuration loaded successfully from {config_path}")
            return config
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        raise

def login_and_prepare_driver(portal, config):
    """Open browser and wait for manual login"""
    logger.info(f"Starting {portal} driver...")
    try:
        driver = webdriver.Chrome()
        portal_url = f'https://www.{portal.lower()}.com/'
        logger.info(f"Opening {portal_url}")
        driver.get(portal_url)
        
        print(f"\n{'='*60}")
        print(f"Please log in to {portal} in the browser window.")
        print(f"After logging in, press Enter here to continue...")
        print(f"{'='*60}\n")
        
        input()  # Wait for manual login
        logger.info(f"Manual login completed for {portal}")
        return driver
    except Exception as e:
        logger.error(f"Error initializing driver: {e}")
        raise

def search_jobs(driver, config):
    """Search for jobs based on config filters"""
    portal = config['job_portal'].lower()
    filters = config['filters']
    jobs = []
    
    logger.info(f"Starting job search on {portal}")
    logger.info(f"Search filters: {filters}")
    
    try:
        if portal == 'linkedin':
            return search_linkedin_jobs(driver, config, filters)
        elif portal == 'indeed':
            return search_indeed_jobs(driver, config, filters)
        else:
            logger.warning(f"Portal {portal} not supported yet")
            return []
    except Exception as e:
        logger.error(f"Error during job search: {e}")
        return []

def search_linkedin_jobs(driver, config, filters):
    """LinkedIn specific job search"""
    jobs = []
    try:
        logger.info("Navigating to LinkedIn jobs page...")
        driver.get('https://www.linkedin.com/jobs/')
        random_delay(*config['delay_range_sec'])
        
        # Try to find job cards - Updated selectors for current LinkedIn
        logger.info("Looking for job listings...")
        
        # Common LinkedIn job card selectors
        job_card_selectors = [
            '.job-card-container',
            '[data-job-id]',
            '.jobs-search__results-list li',
            '.job-search-card'
        ]
        
        job_cards = []
        for selector in job_card_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    job_cards = elements
                    logger.info(f"Found {len(job_cards)} job cards using selector: {selector}")
                    break
            except:
                continue
        
        if not job_cards:
            logger.warning("No job cards found. LinkedIn may have updated their page structure.")
            logger.info("Please inspect the page and update the selectors in search_linkedin_jobs()")
            return []
        
        logger.info(f"Processing {len(job_cards)} job listings...")
        
        for idx, card in enumerate(job_cards[:10]):  # Limit to first 10 for testing
            try:
                # Try multiple selector strategies
                title = None
                company = None
                link = None
                
                # Try to get title
                title_selectors = ['.job-title', '[data-test="job-title"]', '.job-card__title']
                for sel in title_selectors:
                    try:
                        title_elem = card.find_element(By.CSS_SELECTOR, sel)
                        title = title_elem.text
                        if title:
                            break
                    except:
                        continue
                
                # Try to get company
                company_selectors = ['.company-name', '[data-test="company-name"]', '.job-card__company']
                for sel in company_selectors:
                    try:
                        company_elem = card.find_element(By.CSS_SELECTOR, sel)
                        company = company_elem.text
                        if company:
                            break
                    except:
                        continue
                
                # Try to get link
                try:
                    link_elem = card.find_element(By.CSS_SELECTOR, 'a')
                    link = link_elem.get_attribute('href')
                except:
                    link = None
                
                if title and company:
                    job = {
                        'title': title,
                        'company': company,
                        'link': link or 'N/A',
                        'portal': 'linkedin'
                    }
                    jobs.append(job)
                    logger.info(f"Found job {idx+1}: {title} at {company}")
                else:
                    logger.debug(f"Skipped job card {idx+1} - missing title or company")
                    
            except Exception as e:
                logger.debug(f"Error processing job card {idx+1}: {e}")
                continue
        
        logger.info(f"Job search completed. Found {len(jobs)} jobs.")
        return jobs
        
    except Exception as e:
        logger.error(f"Error in LinkedIn search: {e}")
        return []

def search_indeed_jobs(driver, config, filters):
    """Indeed specific job search - placeholder"""
    logger.info("Indeed search not yet implemented")
    return []
