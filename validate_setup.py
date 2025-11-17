#!/usr/bin/env python3
"""
Setup Validation Script for Job Auto-Applier

Validates that all dependencies and configurations are correctly installed.
Run this before using the tool for the first time.

Usage:
    python validate_setup.py
"""

import sys
import os
import json
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_header():
    """Print script header"""
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}Job Auto-Applier Setup Validator{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def check_python_version():
    """Check if Python version is 3.6 or higher"""
    print("1. Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"   {Colors.GREEN}✓ Python {version.major}.{version.minor}.{version.micro}{Colors.RESET}\n")
        return True
    else:
        print(f"   {Colors.RED}✗ Python 3.6+ required (found {version.major}.{version.minor}){Colors.RESET}\n")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("2. Checking required packages...")
    required = ['selenium', 'webdriver_manager', 'flask']
    all_ok = True
    
    for package in required:
        try:
            __import__(package)
            print(f"   {Colors.GREEN}✓ {package}{Colors.RESET}")
        except ImportError:
            print(f"   {Colors.RED}✗ {package} - NOT INSTALLED{Colors.RESET}")
            all_ok = False
    
    if not all_ok:
        print(f"\n   {Colors.YELLOW}Run: pip install -r requirements.txt{Colors.RESET}\n")
    else:
        print()
    
    return all_ok

def check_config_file():
    """Check if config.json exists and is valid"""
    print("3. Checking config.json...")
    config_path = Path('config.json')
    
    if not config_path.exists():
        print(f"   {Colors.RED}✗ config.json not found{Colors.RESET}\n")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"   {Colors.GREEN}✓ config.json is valid JSON{Colors.RESET}")
        
        # Check required fields
        required_fields = ['job_portal', 'filters', 'resume_path']
        missing = [f for f in required_fields if f not in config]
        
        if missing:
            print(f"   {Colors.RED}✗ Missing fields: {', '.join(missing)}{Colors.RESET}\n")
            return False
        else:
            print(f"   {Colors.GREEN}✓ All required fields present{Colors.RESET}\n")
            return True
    except json.JSONDecodeError as e:
        print(f"   {Colors.RED}✗ Invalid JSON: {str(e)}{Colors.RESET}\n")
        return False

def check_resume_file():
    """Check if resume file exists"""
    print("4. Checking resume file...")
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        resume_path = config.get('resume_path', '')
        if not resume_path:
            print(f"   {Colors.YELLOW}⚠ resume_path not configured{Colors.RESET}\n")
            return True
        
        resume_file = Path(resume_path)
        if resume_file.exists():
            print(f"   {Colors.GREEN}✓ Resume found: {resume_path}{Colors.RESET}\n")
            return True
        else:
            print(f"   {Colors.YELLOW}⚠ Resume not found: {resume_path}{Colors.RESET}")
            print(f"   {Colors.YELLOW}   Place your resume in the resume/ folder{Colors.RESET}\n")
            return False
    except Exception as e:
        print(f"   {Colors.RED}✗ Error checking resume: {str(e)}{Colors.RESET}\n")
        return False

def check_resume_folder():
    """Check if resume folder exists"""
    print("5. Checking resume folder...")
    resume_dir = Path('resume')
    
    if resume_dir.exists() and resume_dir.is_dir():
        files = list(resume_dir.glob('*'))
        print(f"   {Colors.GREEN}✓ resume/ folder exists{Colors.RESET}")
        if files:
            print(f"   {Colors.GREEN}✓ Contains {len(files)} file(s){Colors.RESET}\n")
        else:
            print(f"   {Colors.YELLOW}⚠ resume/ folder is empty{Colors.RESET}\n")
        return True
    else:
        print(f"   {Colors.RED}✗ resume/ folder not found{Colors.RESET}\n")
        return False

def check_required_files():
    """Check if all required source files exist"""
    print("6. Checking required files...")
    required_files = [
        'scraper.py',
        'apply_jobs.py',
        'logger.py',
        'run.py',
        'requirements.txt'
    ]
    
    all_ok = True
    for file in required_files:
        if Path(file).exists():
            print(f"   {Colors.GREEN}✓ {file}{Colors.RESET}")
        else:
            print(f"   {Colors.RED}✗ {file} - NOT FOUND{Colors.RESET}")
            all_ok = False
    
    print()
    return all_ok

def print_summary(results):
    """Print validation summary"""
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"Validation Results: {passed}/{total} checks passed")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    if failed == 0:
        print(f"{Colors.GREEN}✓ All checks passed! You're ready to run the tool.{Colors.RESET}\n")
        print(f"Next steps:")
        print(f"  1. Configure your search filters in config.json")
        print(f"  2. Run: python run.py")
        print(f"  3. Log in when the browser opens")
        print(f"  4. Check logs in job_scraper.log\n")
        return True
    else:
        print(f"{Colors.RED}✗ {failed} check(s) failed. Please fix the issues above.{Colors.RESET}\n")
        return False

def main():
    """Run all validation checks"""
    print_header()
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Config File': check_config_file(),
        'Resume File': check_resume_file(),
        'Resume Folder': check_resume_folder(),
        'Required Files': check_required_files()
    }
    
    success = print_summary(results)
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
