import { test, expect } from '@playwright/test';

test('weather agent app loads', async ({ page }) => {
  await page.goto('/', { waitUntil: 'domcontentloaded', timeout: 60000 });

  await expect(page).toHaveTitle(/Weather Agent/i);
});
