# Site Health Checker

A lightweight website health monitoring tool built with Python and Playwright.

## Features

- Opens a website and checks if it loads successfully
- Measures page load time
- Captures browser console errors
- Takes a screenshot
- Generates a structured JSON report
- Handles failures gracefully

## Project Structure

- `checker.py` - core site checking logic
- `main.py` - entry point
- `screenshots/` - saved screenshots
- `reports/` - generated JSON reports

## Installation

```bash
pip install -r requirements.txt
playwright install