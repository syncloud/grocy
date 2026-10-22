import { test as base, expect } from '@playwright/test'
import * as path from 'node:path'
import { shoot } from './screenshot'

export const test = base.extend<{ failureScreenshot: void }>({
  failureScreenshot: [
    async ({ page }, use, info) => {
      await use()
      if (info.status !== info.expectedStatus) {
        console.log(`failure url: ${page.url()}`)
        await shoot(page, `failed-${path.basename(info.file, '.spec.ts')}-line-${info.line}`)
      }
    },
    { auto: true },
  ],
})

export { expect }
