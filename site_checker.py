from playwright.sync_api import sync_playwright
from datetime import datetime
import os, json

def check_site(url):
    console_errors = []
    title = None
    error_message = None
    filename = None
    domain = url.split("//")[-1].split(".")[0]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = f"reports/{domain}_{timestamp}.json"
    status = "failed"
    def handle_console(msg):
        if msg.type == "error":
            console_errors.append(msg.text)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page() 
        page.on("console", handle_console)
        try:
            page.goto(url, wait_until="load")
    
            title = page.title()
            os.makedirs("screenshots", exist_ok=True)
          
            filename = f"screenshots/{domain}_{timestamp}.png"
            page.screenshot(path=filename)

            status = "success"
        except Exception as e:
            error_message = str(e)
        finally:           
            browser.close()
    report = {
        "url": url,
        "status": status,
        "title": title,
        "console_errors": console_errors,
        "screenshot": filename,
        "error_message": error_message
    }
    os.makedirs("reports", exist_ok=True)
    with open(report_filename, "w") as f:
        json.dump(report, f, indent=4)
    return report

if __name__ == "__main__":
    result  =check_site("https://example.com")
    print("Report:", result)