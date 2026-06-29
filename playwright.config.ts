import { defineConfig } from '@playwright/test';

// 🌍 ONE source of truth for all environments
const BASE_URL =
  process.env.BASE_URL || 'http://127.0.0.1:8501';

export default defineConfig({
  testDir: './tests/e2e',

  // ⏱ stability for CI + cloud
  timeout: 90_000,

  expect: {
    timeout: 10_000,
  },

  // 🔁 retry only in CI/cloud
  retries: process.env.CI ? 2 : 0,

  // ⚡ parallel execution for speed (safe for stateless UI apps like Streamlit)
  fullyParallel: true,

  use: {
    baseURL: BASE_URL,

    // works in:
    // - local (visible debugging if needed)
    // - CI (headless)
    // - cloud runners
    headless: true,

    // 🧠 debugging tools (VERY important for CI failures)
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',

    // 🧼 stability for slow cloud environments
    actionTimeout: 0,
    navigationTimeout: 60_000,
  },

  reporter: [
    ['list'],
    ['html', { open: 'never' }]
  ],
});