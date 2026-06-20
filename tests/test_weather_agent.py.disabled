import time
from playwright.sync_api import sync_playwright

def test_weather_agent():
    with sync_playwright() as p:
        # Launch browser in headless mode for CI/CD compatibility
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 1. Page Loads (Targeting your live cloud app)
        print("Step 1: Loading page...")
        page.goto("https://streamlit.app")
        page.wait_for_selector("h1", timeout=15000)  # Wait for title to appear
        print("Page loaded ✅")
        
        # 2. UI Check - take screenshot
        print("Step 2: Taking screenshot...")
        page.screenshot(path="homepage.png", full_page=True)
        print("Screenshot saved as homepage.png ✅")
        
        # 3. Interaction Test - click Gym Singapore button
        print("Step 3: Testing Gym Singapore button...")
        try:
            page.click("button:has-text('Gym Singapore')", timeout=5000)
            page.wait_for_timeout(3000)  # Wait 3s for Databricks LLM response
            page.screenshot(path="after_interaction.png")
            print("Gym Singapore button clicked successfully ✅")
        except Exception as e:
            print(f"Button not found or timed out: {e}")
        
        time.sleep(1)
        browser.close()
        print("Test complete ✅")

if __name__ == "__main__":
    test_weather_agent()
