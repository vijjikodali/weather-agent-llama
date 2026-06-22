import { test, expect } from '@playwright/test';

test('Weather app loads and responds correctly', async ({ page }) => {
  // Open app
  await page.goto('/');

  // Wait for Streamlit UI to load
  await page.waitForTimeout(4000);

  // Get page content
  const bodyText = await page.locator('body').innerText();

  // 1. App should load
  expect(bodyText).toBeTruthy();
  expect(bodyText.length).toBeGreaterThan(20);

  // 2. Basic UI validation (NOT AI dependent)
  const lowerText = bodyText.toLowerCase();

  expect(
    lowerText.includes('weather') ||
    lowerText.includes('streamlit') ||
    lowerText.includes('input')
  ).toBeTruthy();

  // 3. Ensure app is not crashed (important CI check)
  expect(lowerText.includes('error')).toBeFalsy();
});