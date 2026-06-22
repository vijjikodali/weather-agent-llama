import { test, expect } from '@playwright/test';

test('weather agent app loads', async ({ page }) => {
  await page.goto('/');

  // IMPORTANT: wait for app to fully load
  await page.waitForLoadState('networkidle');

  // safer check (NOT exact text)
  await expect(page.locator('body')).toContainText('Weather');
});