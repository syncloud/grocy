import { test } from '../helpers/fixtures'
import { login, locations, masterData, products, purchase, stockOverview } from '../helpers/grocy'

test('stock survives the upgrade and can grow', async ({ page }) => {
  await test.step('login', () => login(page, 'post-upgrade'))
  await test.step('stock overview survived', () => stockOverview(page, 10, 'post-upgrade-survived'))
  await test.step('master data', () => masterData(page, 'post-upgrade'))
  await test.step('locations', () => locations(page, 10, 'post-upgrade'))
  await test.step('products', () => products(page, 10, 20, 'post-upgrade'))
  await test.step('purchase', () => purchase(page, 10, 20, 'post-upgrade'))
  await test.step('stock overview', () => stockOverview(page, 20, 'post-upgrade'))
})
