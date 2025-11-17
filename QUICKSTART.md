# Quick Start Guide

⚡ **Get started with Job Auto-Applier in 5 minutes**

## 0. Prerequisites

Before starting, make sure you have:
- ✅ Python 3.6+ installed (`python --version`)
- ✅ Chrome/Chromium browser installed
- ✅ Your resume in PDF or DOCX format
- ✅ A LinkedIn or Indeed account

## 1. Setup (2 minutes)

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/balayyalegendmovie-spec/job-auto-applier.git
cd job-auto-applier

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Prepare Your Resume (1 minute)

```bash
# Copy your resume to the resume folder
cp /path/to/your/resume.pdf resume/my_resume.pdf
```

Or manually:
1. Copy your resume file (PDF or DOCX)
2. Paste it into the `resume/` folder
3. Remember the filename (you'll need it next)

## 3. Configure (1 minute)

Open `config.json` and update:

```json
{
  "job_portal": "LinkedIn",  // or "Indeed"
  "filters": {
    "keywords": ["Python Developer", "Software Engineer"],
    "location": "Your City",
    "experience_level": "Entry level"
  },
  "resume_path": "./resume/my_resume.pdf",  // Match your filename!
  "max_applications": 10  // Start small for testing
}
```

**Quick Config Tips:**
- `keywords`: Use actual job titles from LinkedIn/Indeed
- `location`: Try "New York", "Remote", "San Francisco"
- `resume_path`: Must match exactly (case-sensitive on Linux/Mac)
- `max_applications`: Try 5-10 for first run

## 4. Run (1 minute)

```bash
python run.py
```

You'll see:
```
[INFO] Starting job search on LinkedIn
[INFO] Manual login required - please log in to LinkedIn in the browser window
[INFO] Waiting for manual login completion...
```

## 5. Manual Login

When the browser opens:

1. ✅ **Log in** to LinkedIn/Indeed manually
2. ✅ Complete any **CAPTCHA** if prompted
3. ✅ Verify you're on the jobs search page
4. ✅ **Press Enter** in the terminal when done

The tool will then:
- Search for jobs matching your filters
- Apply to matching positions
- Upload your resume
- Track all applications

## 6. Monitor Results

Check the outputs:

```bash
# View the log file
cat job_scraper.log  # Linux/Mac
type job_scraper.log  # Windows

# Open the CSV in Excel/Sheets
open application_log.csv  # Mac
start application_log.csv  # Windows
```

**CSV Columns:**
- Date: When application was made
- Job Title: The position applied for
- Company: Company name
- Status: Success/Failed
- Notes: Any errors or issues

## Common Issues & Fixes

### "ModuleNotFoundError: No module named 'selenium'"
**Fix:**
```bash
pip install -r requirements.txt
```

### "Chrome driver not found"
**Fix:**
```bash
pip install --upgrade webdriver-manager
```

### "Manual login failed / CAPTCHA won't load"
**Fix:**
1. Close the browser window
2. Wait 10 seconds
3. Run `python run.py` again
4. Log in more slowly this time

### "Resume not uploading"
**Fix:**
1. Check resume path in config.json is correct
2. Ensure resume file exists: `ls resume/my_resume.pdf`
3. Try a different resume format (PDF instead of DOCX)

### "No jobs found"
**Fix:**
1. Check your keywords (search for them manually first)
2. Try a bigger location ("United States" instead of a city)
3. Increase experience level range
4. Check logs for selector errors

## Next Steps

✅ **First Run Success?** Try:
- `max_applications`: 20 (increase batch size)
- `delay_range_sec`: [3, 8] (faster processing)
- Different keywords or locations

✅ **Want to Extend?** Check out:
- `README.md` - Full documentation
- Extending to new job portals
- Custom selector modifications

✅ **Having Issues?** See:
- Troubleshooting section in `README.md`
- GitHub Issues: https://github.com/balayyalegendmovie-spec/job-auto-applier/issues

## Real Quick Example

### Step-by-step for LinkedIn Internships:

```json
{
  "job_portal": "LinkedIn",
  "filters": {
    "keywords": ["Software Internship", "AI Internship"],
    "location": "United States",
    "experience_level": "Internship"
  },
  "resume_path": "./resume/resume_2024.pdf",
  "max_applications": 5
}
```

Run:
```bash
python run.py
# -> Logs in (you handle CAPTCHA)
# -> Searches for internships
# -> Applies to 5 matching positions
# -> Creates application_log.csv
```

## Performance Expectations

- Setup: ~2 minutes
- First run: ~3-5 minutes (includes manual login)
- Subsequent runs: ~2-3 minutes per 10 applications
- Most time is: Waiting between actions (for bot detection safety)

## Safety Reminders

⚠️ **Important:**
- Use **reasonable delays** (don't change to 0-1 seconds)
- Apply only to jobs you're **genuinely interested** in
- Job portals **may change** and break selectors
- This is **for learning/testing only**
- Check the job portal's **terms of service**

## Got It? Let's Go!

```bash
# You're ready!
python run.py
```

For detailed documentation, see `README.md`.

Good luck with your job search! 🚀
