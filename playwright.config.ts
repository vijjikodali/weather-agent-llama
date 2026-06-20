import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 60000,

  use: {
    baseURL: 'http://127.0.0.1:8501',
    headless: true,
  },

  webServer: {
    command: 'ENV=ci python -m streamlit run app.py --server.port 8501 --server.headless true',
    url: 'http://127.0.0.1:8501',
    timeout: 90000,
    reuseExistingServer: !process.env.CI,
  },
});
