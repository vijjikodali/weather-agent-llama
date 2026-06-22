import { test, expect } from '@playwright/test';

test('Weather app loads and responds correctly', async ({ page }) => {
  await page.goto('/');

  // Wait for Streamlit to fully render
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(6000);

  // Get page content
  const bodyText = await page.locator('body').innerText();

  // 1. App should load
  expect(bodyText).toBeTruthy();
  expect(bodyText.length).toBeGreaterThan(20);

  const lowerText = bodyText.toLowerCase();

  // 2. UI sanity check (safe for CI)
  expect(
    lowerText.includes('weather') ||
    lowerText.includes('streamlit') ||
    lowerText.includes('input') ||
    lowerText.includes('app')
  ).toBeTruthy();

  // 3. Ensure app is not crashed
  expect(lowerText).not.toContain('traceback');
  expect(lowerText).not.toContain('error');
  expect(lowerText).not.toContain('exception');
});