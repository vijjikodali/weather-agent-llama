import { test, expect } from '@playwright/test';

test('weather agent app loads', async ({ page }) => {
  await page.goto('/', { waitUntil: 'domcontentloaded' });

  await page.waitForLoadState('networkidle');

  await expect(page.locator('body')).toBeVisible();
});