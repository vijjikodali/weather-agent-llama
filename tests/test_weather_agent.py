from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False so you can see it
    page = browser.new_page()
    
    # 1. Page Loads
    print("Step 1: Loading page...")
    page.goto("http://localhost:8501")
    page.wait_for_load_state("networkidle")
    print("Page loaded ✅")
    
    # 2. UI Check - take screenshot
    print("Step 2: Taking screenshot...")
    page.screenshot(path="homepage.png", full_page=True)
    print("Screenshot saved as homepage.png ✅")
    
    # 3. Interaction Test - click Analyze button
    print("Step 3: Testing Analyze button...")
    try:
        page.click("button:has-text('Analyze')", timeout=5000)
        page.wait_for_timeout(2000)  # wait 2s for result
        page.screenshot(path="after_analyze.png")
        print("Analyze button clicked ✅")
    except:
        print("Analyze button not found - check button text in your Streamlit app")
    
    time.sleep(1)
    browser.close()
    print("Test complete ✅")
