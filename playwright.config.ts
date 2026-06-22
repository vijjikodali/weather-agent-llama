import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 60000,

  use: {
    baseURL: 'http://127.0.0.1:8501',
    headless: true,
  },

  reporter: [['html', { open: 'never' }]],

  // ======================
  // START STREAMLIT APP
  // ======================
  webServer: {
    command: 'python -m streamlit run app.py --server.port 8501 --server.address 127.0.0.1',
    url: 'http://127.0.0.1:8501',
    reuseExistingServer: false,
    timeout: 120 * 1000
  }
});
