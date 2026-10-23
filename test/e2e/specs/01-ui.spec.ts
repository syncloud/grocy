import { test } from '../helpers/fixtures'
import { login, locations, masterData, products, purchase, stockOverview } from '../helpers/grocy'

test('stock a fresh install through the ui', async ({ page }) => {
  await test.step('login', () => login(page, 'ui'))
  await test.step('master data', () => masterData(page, 'ui'))
  await test.step('locations', () => locations(page, 10, 'ui'))
  await test.step('products', () => products(page, 0, 100, 'ui'))
  await test.step('purchase', () => purchase(page, 0, 100, 'ui'))
  await test.step('stock overview', () => stockOverview(page, 100, 'ui'))
})
