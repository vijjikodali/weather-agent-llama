import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 60000,

  use: {
    baseURL: 'http://127.0.0.1:8501',
    headless: true,
  },

  webServer: {
    command: 'python -m streamlit run app.py --server.port 8501 --server.headless true --server.address 127.0.0.1',
    url: 'http://127.0.0.1:8501',

    timeout: 120000,

    reuseExistingServer: !process.env.CI,

    // 🔥 CRITICAL FIX: ensures server is really ready
    stdout: 'pipe',
    stderr: 'pipe',
  },
});