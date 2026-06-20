import { test, expect } from '@playwright/test';

test('AI weather response validation', async ({ page }) => {
  await page.goto('/');

  await page.getByPlaceholder('Ask weather...').fill('Can I go to beach in Mumbai today?');
  await page.keyboard.press('Enter');

  const response = page.locator('[data-testid="stChatMessage"]').last();

  await expect(response).toBeVisible();

  const text = await response.textContent();

  // 🔥 AI VALIDATION RULES

  expect(text).toBeTruthy();
  expect(text!.length).toBeGreaterThan(10);

  expect(
    text!.toLowerCase().includes('mumbai') ||
    text!.toLowerCase().includes('weather') ||
    text!.toLowerCase().includes('rain') ||
    text!.toLowerCase().includes('temperature')
  ).toBeTruthy();
});