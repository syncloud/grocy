import { Page, expect } from '@playwright/test'
import { env } from './env'
import { shoot } from './screenshot'

function sidebar(page: Page) {
  return page.locator('.navbar-sidenav')
}

function masterDataMenu(page: Page) {
  return page.locator('#sub-nav-manage-master-data')
}

function pad(i: number): string {
  return i.toString().padStart(3, '0')
}

export function productName(i: number): string {
  return `Product-${pad(i)}`
}

export async function login(page: Page, screenshot: string) {
  await page.goto('/')
  const username = page.locator('#username')
  await expect(username).toBeVisible()
  await username.fill(env('PLAYWRIGHT_DEVICE_USER'))
  const password = page.locator('#password')
  await password.fill(env('PLAYWRIGHT_DEVICE_PASSWORD'))
  await shoot(page, `${screenshot}-login`)
  await password.press('Enter')
  await expect(page.locator('h2.title', { hasText: 'Stock overview' })).toBeVisible()
  await shoot(page, `${screenshot}-main`)
}

export async function masterData(page: Page, screenshot: string) {
  await sidebar(page).getByRole('link', { name: 'Manage master data' }).click()
  await expect(masterDataMenu(page)).toBeVisible()
  await shoot(page, `${screenshot}-master-data`)
}

export async function locations(page: Page, count: number, screenshot: string) {
  await masterDataMenu(page).getByRole('link', { name: 'Locations', exact: true }).click()
  const table = page.locator('#locations-table')
  await expect(table).toBeVisible()
  for (let i = 0; i < count; i++) {
    const name = `Location-${pad(i)}`
    const row = table.getByRole('cell', { name, exact: true })
    if (await row.count() > 0) {
      continue
    }
    await page.getByRole('link', { name: 'Add', exact: true }).click()
    const dialog = page.frameLocator('.bootbox iframe')
    await dialog.locator('#name').fill(name)
    await dialog.locator('#description').fill(`${name} description`)
    await dialog.locator('#save-location-button').click()
    await expect(row).toBeVisible()
  }
  await shoot(page, `${screenshot}-locations`)
}

export async function products(page: Page, from: number, to: number, screenshot: string) {
  await masterDataMenu(page).getByRole('link', { name: 'Products', exact: true }).click()
  const table = page.locator('#products-table')
  await expect(table).toBeVisible()
  for (let i = from; i < to; i++) {
    const product = productName(i)
    const row = table.getByRole('cell', { name: product, exact: true })
    if (await row.count() > 0) {
      continue
    }
    await page.getByRole('link', { name: 'Add', exact: true }).click()
    const name = page.locator('#name')
    await expect(name).toBeVisible()
    await name.fill(product)
    await page.locator('#location_id').selectOption({ label: 'Fridge' })
    await page.locator('#qu_id_stock').selectOption({ label: 'Pack' })
    await page.getByRole('button', { name: 'Save & return to products' }).click()
    await expect(row).toBeVisible()
  }
  await shoot(page, `${screenshot}-products`)
}

export async function purchase(page: Page, from: number, to: number, screenshot: string) {
  await sidebar(page).locator('a[href$="/purchase"]').click()
  const input = page.locator('#product_id_text_input')
  await expect(input).toBeVisible()
  const dueDate = `${new Date().getFullYear() + 1}-01-01`
  for (let i = from; i < to; i++) {
    await purchaseOne(page, productName(i), dueDate)
  }
  await shoot(page, `${screenshot}-purchase`)
}

async function purchaseOne(page: Page, product: string, dueDate: string) {
  const input = page.locator('#product_id_text_input')
  await input.fill('')
  await input.pressSequentially(product)
  await page.getByRole('link', { name: product, exact: true }).click()
  await expect(page.locator('#productcard-product-name')).toHaveText(product)
  const amount = page.locator('#display_amount')
  await expect(amount).toBeFocused()
  await amount.fill('10')
  await expect(amount).toHaveValue('10')
  const date = page.locator('#best_before_date input')
  await date.click()
  await date.press('Control+a')
  await date.pressSequentially(dueDate)
  await date.press('Tab')
  await expect(amount).toHaveValue('10')
  await page.locator('#save-purchase-button').click()
  await expect(page.locator('.toast-success', { hasText: product })).toBeVisible()
  await expect(input).toHaveValue('')
}

export async function stockOverview(page: Page, expectedProducts: number, screenshot: string) {
  await sidebar(page).locator('a[href$="/stockoverview"]').click()
  await expect(page.locator('#info-current-stock')).toHaveText(new RegExp(`^${expectedProducts} Products\\b`))
  await shoot(page, `${screenshot}-stock-overview`)
}
