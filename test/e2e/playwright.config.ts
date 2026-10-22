import { defineConfig, devices } from '@playwright/test'

const domain = process.env.PLAYWRIGHT_DOMAIN ?? 'buster.com'
const app = process.env.PLAYWRIGHT_APP ?? 'grocy'

export default defineConfig({
  testDir: './specs',
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  reporter: 'list',
  timeout: 3_600_000,
  expect: { timeout: 30_000 },
  use: {
    actionTimeout: 60_000,
    navigationTimeout: 120_000,
    baseURL: `https://${app}.${domain}`,
    ignoreHTTPSErrors: true,
    trace: 'off',
    video: 'off',
    screenshot: 'off',
  },
  projects: [
    {
      name: 'desktop',
      use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 960 } },
    },
  ],
})
