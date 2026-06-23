import { defineConfig } from '@playwright/test';

// 1. Fallback to 8501 if process.env.PORT is undefined
const PORT = process.env.PORT || '8501';
const BASE_URL = `http://127.0.0.1:${PORT}`;

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 60_000,

  use: {
    baseURL: BASE_URL,
    headless: true,
  },

  reporter: [['html', { open: 'never' }]],
  
  webServer: {
    // 2. Use the dynamic PORT variable in the command line string
    command: `streamlit run app.py --server.port ${PORT} --server.address 127.0.0.1 --server.headless true --browser.gatherUsageStats false`,

    // 3. Match the target URL perfectly with the dynamic base URL
    url: BASE_URL,

    // 4. Set to true for local development speed; false for clean CI environments
    reuseExistingServer: !process.env.CI,

    timeout: 60 * 1000, // 60 seconds is more than enough for Streamlit to boot

    // 5. 'inherit' routes Streamlit crashes/errors directly to your terminal console
    stdout: 'ignore',
    stderr: 'inherit',
  }
});
