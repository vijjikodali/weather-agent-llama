from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("http://localhost:8501")

    print("App opened successfully")

    page.screenshot(path="screenshots/homepage.png")

    browser.close()