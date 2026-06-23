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
  command: `bash -c "fuser -k 8501/tcp || true; streamlit run app.py --server.port 8501 --server.address 127.0.0.1 --server.headless true"`,

  url: BASE_URL,

  reuseExistingServer: false,

  timeout: 180 * 1000,
  stdout: 'pipe',
  stderr: 'pipe',

  ignoreHTTPSErrors: true,
}
});
