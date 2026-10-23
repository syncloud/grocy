import { test } from '../helpers/fixtures'
import { login, locations, masterData, products, purchase, stockOverview } from '../helpers/grocy'

test('stock the released version before upgrade', async ({ page }) => {
  await test.step('login', () => login(page, 'pre-upgrade'))
  await test.step('master data', () => masterData(page, 'pre-upgrade'))
  await test.step('locations', () => locations(page, 10, 'pre-upgrade'))
  await test.step('products', () => products(page, 0, 10, 'pre-upgrade'))
  await test.step('purchase', () => purchase(page, 0, 10, 'pre-upgrade'))
  await test.step('stock overview', () => stockOverview(page, 10, 'pre-upgrade'))
})
