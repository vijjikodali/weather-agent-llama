import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 60_000,

  use: {
    baseURL: 'http://127.0.0.1:8501',
    headless: true,
  },

  reporter: [['html', { open: 'never' }]],

  // ======================
  // STREAMLIT SERVER SETUP
  // ======================
  webServer: {
    command: 'bash -c "streamlit run app.py --server.port 8501 --server.address 127.0.0.1 --server.headless true"',
    
    url: 'http://127.0.0.1:8501',

    // IMPORTANT: helps avoid flaky startup failures
    reuseExistingServer: !process.env.CI,

    timeout: 180 * 1000,

    // 🔥 HEALTH CHECK (critical improvement)
    stdout: 'pipe',
    stderr: 'pipe',

    // Wait strategy (Playwright will poll URL)
    ignoreHTTPSErrors: true
  }
});
