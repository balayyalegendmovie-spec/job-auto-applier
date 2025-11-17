# run.py - Main entry point for Job Auto Applier
import logging
from scraper import load_config, login_and_prepare_driver, search_jobs
from apply_jobs import apply_batch_jobs

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main_automation_process():
    """
    Main automation workflow:
    1. Load configuration
    2. Open browser and perform manual login
    3. Search for jobs based on filters
    4. Apply to jobs automatically
    5. Generate report
    """
    driver = None
    try:
        logger.info("="*60)
        logger.info("Job Auto Applier - Starting Process")
        logger.info("="*60)
        
        # Step 1: Load configuration
        logger.info("Step 1: Loading configuration...")
        config = load_config()
        logger.info(f"Configuration loaded successfully")
        logger.info(f"  Job Portal: {config['job_portal']}")
        logger.info(f"  Resume Path: {config.get('resume_path', 'Not set')}")
        
        # Step 2: Initialize driver and manual login
        logger.info("\nStep 2: Initializing browser...")
        driver = login_and_prepare_driver(config['job_portal'], config)
        logger.info("Browser initialized successfully")
        
        # Step 3: Search for jobs
        logger.info("\nStep 3: Searching for jobs...")
        jobs = search_jobs(driver, config)
        logger.info(f"Found {len(jobs)} matching jobs")
        
        if not jobs:
            logger.warning("No jobs found to apply to. Exiting.")
            return
        
        # Step 4: Apply to jobs
        logger.info("\nStep 4: Starting application process...")
        max_applications = config.get('max_applications', None)
        if max_applications:
            logger.info(f"Will apply to maximum {max_applications} jobs")
        
        results = apply_batch_jobs(driver, jobs, config, max_applications=max_applications)
        
        # Step 5: Print summary
        logger.info("\nFinal Summary:")
        logger.info(f"  Total Jobs Found: {len(jobs)}")
        logger.info(f"  Successful Applications: {results['success']}")
        logger.info(f"  Failed Applications: {results['failed']}")
        logger.info(f"  Manual Required: {results['manual_required']}")
        logger.info(f"  Partial Applications: {results['partial']}")
        logger.info("\nCheck 'application_log.csv' and 'job_scraper.log' for detailed results")
        logger.info("="*60)
        
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        logger.error("Please ensure config.json exists in the project directory")
    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}", exc_info=True)
    finally:
        # Cleanup
        if driver:
            logger.info("Closing browser...")
            driver.quit()
            logger.info("Browser closed")
        logger.info("\nProcess completed")
        logger.info("="*60)

if __name__ == '__main__':
    main_automation_process()
