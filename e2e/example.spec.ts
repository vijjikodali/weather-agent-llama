import { test, expect } from '@playwright/test';

test('Weather app loads successfully', async ({ page }) => {
  await page.goto('/');

  // wait for app
  await page.waitForTimeout(3000);

  const body = await page.locator('body').innerText();

  // basic stability check only
  expect(body.length).toBeGreaterThan(20);
  expect(body).toBeTruthy();

  // UI sanity (NOT AI dependent)
  expect(
    body.toLowerCase().includes('weather') ||
    body.toLowerCase().includes('streamlit')
  ).toBeTruthy();
});