# Job Auto-Applier

A local, free Python-based job application automation tool for learning/testing. Supports LinkedIn and Indeed with auto-fill, resume upload, and comprehensive logging.

## Features

✅ **Local & Free** - Runs entirely on your machine, no cloud hosting or paid APIs  
✅ **Manual Browser Login** - Uses Selenium for secure, bot-friendly login with CAPTCHA support  
✅ **Smart Job Scraping** - Searches jobs based on keywords, location, and experience level  
✅ **Auto-Application** - Automatically fills forms and uploads resumes  
✅ **Comprehensive Logging** - Tracks all applications in CSV and JSON formats  
✅ **Configurable** - Full control via JSON config file  
✅ **Learning-Friendly** - Well-commented code, easy to extend for new job portals  
✅ **Rate Limiting** - 2-10 second randomized delays between actions to avoid bot detection  
✅ **CLI + Optional GUI** - Command-line interface with optional Flask web interface  

## Project Structure

```
job-auto-applier/
├── config.json              # Configuration file (filters, delays, logging)
├── credentials.py           # Credential management (no password storage)
├── scraper.py              # Job scraping with multiple selector strategies
├── apply_jobs.py           # Application automation with form handling
├── logger.py               # Logging system (file, console, CSV)
├── run.py                  # Main workflow orchestration
├── gui.py                  # Optional Flask web GUI
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── resume/                # Folder for resume files (PDF/DOCX)
└── .gitignore            # Git ignore rules
```

## Installation

### Prerequisites
- Python 3.6+ (tested on Python 3.8.10)
- Chrome/Chromium browser
- 50MB disk space

### Step 1: Clone Repository

```bash
git clone https://github.com/balayyalegendmovie-spec/job-auto-applier.git
cd job-auto-applier
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
- Selenium (browser automation)
- WebDriverManager (automatic Chrome driver management)
- Flask (optional GUI)
- Python-dotenv (configuration management)

## Configuration

### Edit `config.json`

```json
{
  "job_portal": "LinkedIn",
  "filters": {
    "keywords": ["Software Intern", "Python"],
    "location": "Bangalore",
    "experience_level": "Internship"
  },
  "resume_path": "./resume/my_resume.pdf",
  "delay_range_sec": [2, 10],
  "max_applications": 10,
  "enable_logging": true,
  "log_file": "job_scraper.log",
  "csv_log_file": "application_log.csv"
}
```

**Configuration Options:**
- `job_portal`: "LinkedIn" or "Indeed"
- `keywords`: List of job titles/keywords to search
- `location`: Target job location
- `experience_level`: "Internship", "Entry level", "Mid level", etc.
- `resume_path`: Full path to your resume PDF or DOCX
- `delay_range_sec`: [min, max] seconds to wait between actions
- `max_applications`: Maximum applications per session
- `enable_logging`: Enable file-based logging
- `log_file`: Path to application log file
- `csv_log_file`: Path to CSV log file

## Quick Start

### 1. Prepare Your Resume

Place your resume in the `resume/` folder:
```
resume/
├── my_resume.pdf
└── alternate_resume.pdf
```

### 2. Update Configuration

Edit `config.json` with your search criteria and resume path.

### 3. Run the Tool

**CLI Mode:**
```bash
python run.py
```

**GUI Mode (Optional):**
```bash
python gui.py
# Then open browser to http://localhost:5000
```

### 4. Manual Login

When prompted:
1. A Chrome browser window will open
2. Log in to LinkedIn/Indeed manually
3. Complete any CAPTCHA challenges
4. Press Enter in terminal to continue

### 5. Monitor Progress

The tool will:
- Log each job search step to console
- Save detailed logs to `job_scraper.log`
- Export application results to `application_log.csv`

## Usage Examples

### Search for Internships on LinkedIn

```json
{
  "job_portal": "LinkedIn",
  "filters": {
    "keywords": ["Software Internship", "Data Science Internship"],
    "location": "United States",
    "experience_level": "Internship"
  },
  "max_applications": 20
}
```

### Search for Entry-Level Roles on Indeed

```json
{
  "job_portal": "Indeed",
  "filters": {
    "keywords": ["Junior Developer"],
    "location": "New York",
    "experience_level": "Entry level"
  },
  "max_applications": 15
}
```

## File Documentation

### `config.json`
Centralized configuration file. Update this before each run.

### `scraper.py`
Handles job portal scraping:
- Multiple CSS selector strategies for robustness
- Automated browser login
- Job filtering based on config
- Error handling and logging

### `apply_jobs.py`
Automates job applications:
- Form detection and auto-fill
- Resume upload handling
- Batch processing support
- Application status tracking

### `logger.py`
Manages all logging:
- Console output with timestamps
- File-based logging
- CSV export for analysis
- Error tracking

### `run.py`
Main orchestration:
- Workflow management
- Configuration loading
- Error handling
- Summary reporting

### `gui.py` (Optional)
Flask web interface:
- Configure filters via web UI
- Monitor live progress
- View historical logs

## Output Files

After running the tool:

### `job_scraper.log`
Detailed text log with timestamps:
```
[2024-01-15 10:30:45] INFO - Starting job search on LinkedIn
[2024-01-15 10:30:50] INFO - Found 45 matching jobs
[2024-01-15 10:31:02] INFO - Applied to: Senior Python Developer at TechCorp
```

### `application_log.csv`
Structured data for spreadsheet analysis:
```csv
Date,Time,Job Title,Company,Location,Status,Notes
2024-01-15,10:31:02,Senior Developer,TechCorp,San Francisco,Success,
2024-01-15,10:31:35,Frontend Engineer,StartupXYZ,Remote,Failed,Application form error
```

## Advanced Features

### Custom Delays
Configure random delays to avoid bot detection:
```json
"delay_range_sec": [5, 15]
```
Will randomly wait 5-15 seconds between each action.

### Batch Processing
Limit applications per session:
```json
"max_applications": 25
```
The tool will stop after 25 successful applications.

### Multiple Resumes
Switch between resumes for different job types:
1. Place multiple resumes in `resume/` folder
2. Update `resume_path` in config before each run
3. Or modify `apply_jobs.py` to automatically select resumes

## Troubleshooting

### Issue: Chrome driver not found
**Solution:** WebDriverManager automatically downloads the driver. If it fails:
```bash
pip install --upgrade webdriver-manager
```

### Issue: "CAPTCHA detected" or manual login fails
**Solution:** The browser window will stay open. Complete the login manually:
1. Log in to LinkedIn/Indeed
2. Complete CAPTCHA if prompted
3. Press Enter in terminal when ready

### Issue: Resume not uploading
**Solutions:**
1. Verify resume path in config.json is correct
2. Ensure resume is PDF or DOCX format
3. Check file permissions
4. Verify form accepts file uploads

### Issue: Jobs not found
**Solutions:**
1. Check keywords match actual job postings
2. Try different location names
3. Review CSS selectors for the portal (may change with updates)
4. Check logs for selector errors

### Issue: "Connection refused" error
**Solution:** Ensure Chrome is not already running or:
```bash
killall chrome  # Linux/Mac
taskkill /F /IM chrome.exe  # Windows
```

## Safety & Legal Considerations

⚠️ **Important:**

1. **For Learning Only** - This tool is designed for personal learning and testing
2. **Respect Terms of Service** - Job portals may have restrictions on automation
3. **Rate Limiting** - Always use delays to avoid overloading servers
4. **No Password Storage** - Credentials are never saved; manual login only
5. **Local Execution** - All data stays on your machine
6. **Ethical Use** - Apply to jobs you're genuinely interested in

## Extending to New Job Portals

To add support for a new job portal (e.g., Glassdoor):

1. **Update `scraper.py`:**
   - Add new portal case in `search_jobs()` function
   - Define CSS selectors for job cards
   - Add parsing logic for job details

2. **Update `apply_jobs.py`:**
   - Add form handling for the new portal
   - Define resume upload selectors
   - Add application submission logic

3. **Test thoroughly** before submitting changes

## Development & Testing

### Run in Test Mode
```bash
# Will run with logging enabled and max_applications=1
python run.py --test
```

### View Logs
```bash
# Tail the log file (Linux/Mac)
tail -f job_scraper.log

# Or open the CSV
open application_log.csv  # Mac
start application_log.csv  # Windows
```

## Performance Tips

1. **Optimize Keywords** - Narrow keywords for better results
2. **Adjust Delays** - Shorter delays = faster, longer = safer
3. **Batch Size** - Smaller batches (5-10) are easier to monitor
4. **Resume Format** - Simpler PDFs are faster to upload
5. **Network** - Wired connection is more stable than WiFi

## Known Limitations

- Job portal layouts change frequently; selectors may need updates
- Complex multi-step applications may need manual completion
- Some portals have anti-bot detection that may block automation
- Resume upload may fail on obscure form types
- Requires active monitor (headless mode not supported for security)

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support & Issues

If you encounter issues:

1. Check this README's troubleshooting section
2. Review the logs in `job_scraper.log`
3. Check Python version: `python --version`
4. Ensure all dependencies are installed: `pip list`
5. Open an issue on GitHub with logs and error details

## Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for:
- Compliance with job portal terms of service
- Compliance with local laws and regulations
- Ethical use of automation
- Any consequences resulting from tool usage

Maintainers are not responsible for:
- Account bans or restrictions
- Misuse of the tool
- Legal issues arising from use
- Job portal policy violations

## FAQ

**Q: Is this legal?**  
A: Yes, for personal learning use. But check the job portal's terms - some may restrict automation.

**Q: Will I get banned?**  
A: Unlikely if you use reasonable delays and don't spam. The tool includes rate limiting.

**Q: Can I use this in production?**  
A: No, this is for learning/testing only. For production, contact job portals directly.

**Q: How accurate is job scraping?**  
A: Depends on portal changes. Selectors may break with layout updates.

**Q: Can I run multiple instances?**  
A: Not recommended - they may interfere with each other.

**Q: How do I monitor progress?**  
A: Watch the terminal output and check `job_scraper.log` and `application_log.csv`.

---

**Made with ❤️ for learning automation enthusiasts**

Last Updated: January 2024
