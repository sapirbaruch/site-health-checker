from playwright.sync_api import sync_playwright
from datetime import datetime
from urllib.parse import urlparse
import os
import json
import time


def check_site(url: str) -> dict:
    # Store console errors captured from the browser
    console_errors = []

    # Initialize variables that will be populated during execution
    title = None
    error_message = None
    screenshot_file = None
    load_time_seconds = None
    status = "failed"

    # Parse the URL and extract the domain for file naming
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace(".", "_").replace(":", "_")

    # Create timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Define report and screenshot file paths
    report_file = f"reports/{domain}_{timestamp}.json"
    screenshot_file = f"screenshots/{domain}_{timestamp}.png"

    # Event handler to capture console error messages from the page
    def handle_console(msg):
        if msg.type == "error":
            console_errors.append(msg.text)

    # Ensure output directories exist
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Listen for browser console messages
        page.on("console", handle_console)

        try:
            # Measure page load time
            start_time = time.time()
            page.goto(url, wait_until="load", timeout=10000)
            end_time = time.time()

            load_time_seconds = round(end_time - start_time, 2)

            # Capture page title and screenshot
            title = page.title()
            page.screenshot(path=screenshot_file)

            status = "success"

        except Exception as e:
            # Store error message if navigation fails
            error_message = str(e)

        finally:
            # Ensure browser is always closed
            browser.close()

    # Create structured report with collected data
    report = {
        "url": url,
        "status": status,
        "title": title,
        "console_errors": console_errors,
        "screenshot": screenshot_file if status == "success" else None,
        "error_message": error_message,
        "report_file": report_file,
        "load_time_seconds": load_time_seconds,
    }

    # Save report as JSON
    with open(report_file, "w") as f:
        json.dump(report, f, indent=4)

    return report