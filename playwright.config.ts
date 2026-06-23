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
    command: [
      // 🔥 kills stale streamlit process first (prevents port conflict)
      `bash -c "pkill -f streamlit || true &&`,
      `streamlit run app.py`,
      `--server.port ${PORT}`,
      `--server.address 127.0.0.1`,
      `--server.headless true"`
    ].join(' '),

    url: BASE_URL,

    // 🔥 CI-safe isolation
    reuseExistingServer: false,

    timeout: 180 * 1000,

    stdout: 'pipe',
    stderr: 'pipe',

    // Playwright will poll until app is ready
    ignoreHTTPSErrors: true,
  }
});
