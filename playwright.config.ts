import { defineConfig } from '@playwright/test';

const PORT = process.env.PORT || 8501;
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
  command: `streamlit run app.py --server.port ${PORT} --server.address 127.0.0.1 --server.headless true`,
  url: BASE_URL,

  reuseExistingServer: !process.env.CI,
  timeout: 180 * 1000,

  stdout: 'pipe',
  stderr: 'pipe',

  ignoreHTTPSErrors: true,
}
});
