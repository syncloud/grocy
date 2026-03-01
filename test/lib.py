import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# v4_2 helpers (stable/pre-upgrade grocy UI)

def login_v4_2(selenium, device_user, device_password):
    selenium.open_app()
    selenium.find_by_id("username").send_keys(device_user)
    password = selenium.find_by_id("password")
    password.send_keys(device_password)
    selenium.screenshot('login')
    password.send_keys(Keys.RETURN)
    selenium.find_by_xpath("//h2[contains(.,'Stock overview')]")
    selenium.screenshot('main')


def master_data_v4_2(selenium):
    selenium.find_by_xpath("//span[.='Manage master data']").click()
    selenium.screenshot('master-data')


def locations_v4_2(selenium, count=10):
    selenium.find_by_xpath("//span[.='Locations']").click()
    for i in range(count):
        _dismiss_modals(selenium)
        selenium.find_by_xpath("//a[contains(.,'Add')]").click()
        selenium.driver.switch_to.frame(selenium.find_by_xpath("//iframe"))
        name = f"Location-{i:03d}"
        selenium.click_by(By.ID, "name")
        selenium.find_by_id("name").send_keys(name)
        selenium.find_by_id("description").send_keys(f"{name} description")
        selenium.click_by(By.XPATH, "//button[contains(.,'Save')]")
        selenium.driver.switch_to.default_content()
        selenium.find_by_xpath(f"//td[contains(.,'{name}')]")
    selenium.screenshot('locations')


def products_v4_2(selenium, count=100):
    selenium.find_by_xpath("//span[.='Products']").click()
    for i in range(count):
        selenium.find_by_xpath("//a[contains(.,'Add')]").click()
        product = f"Product-{i:03d}"
        selenium.find_by_id("name").send_keys(product)
        selenium.click_by(By.ID, "location_id")
        selenium.find_by_xpath("//option[.='Fridge']").click()
        selenium.click_by(By.ID, "qu_id_stock")
        selenium.find_by_xpath("//option[.='Pack']").click()
        _scroll_click(selenium, "//button[contains(.,'return to products')]")
        selenium.find_by_xpath("//h2[contains(.,'Products')]")
    selenium.screenshot('products')


def purchase_v4_2(selenium, count=100):
    _dismiss_modals(selenium)
    selenium.click_by(By.XPATH, "//span[.='Purchase']")
    for i in range(count):
        product = f"Product-{i:03d}"
        _purchase_one_v4_2(selenium, product)
    selenium.screenshot('purchase')


def _purchase_one_v4_2(selenium, product, retries=3):
    for attempt in range(retries):
        selenium.driver.execute_script(
            "document.querySelectorAll('.toast').forEach(e => e.remove());"
        )
        product_input = selenium.find_by_id("product_id_text_input")
        product_input.clear()
        product_input.send_keys(product)
        selenium.find_by_xpath(f"//a[contains(., '{product}')]").click()
        _set_amount(selenium, 10)
        if selenium.find_by_id("display_amount").get_attribute("value") != "10":
            continue
        today = datetime.today()
        date_input = selenium.find_by_xpath("//div[@id='best_before_date']/input")
        date_input.click()
        date_input.send_keys(Keys.CONTROL + 'a')
        date_input.send_keys(f'{today.year + 1}-01-01')
        date_input.send_keys(Keys.TAB)
        selenium.find_by_id("save-purchase-button").click()
        selenium.find_by_xpath(f"//div[contains(@class,'toast-success')]//div[contains(.,'{product}')]")
        return
    raise Exception(f"Failed to purchase {product} after {retries} attempts")


def stock_overview_v4_2(selenium, expected_products=100):
    selenium.find_by_xpath("//span[.='Stock overview']").click()
    selenium.find_by_xpath(f"//span[contains(., '{expected_products} Products')]")
    selenium.screenshot('stock-overview')


# v4_5 helpers (current grocy UI)

def _dismiss_modals(selenium):
    selenium.driver.execute_script(
        "document.querySelectorAll('.modal-backdrop, .modal, .bootbox').forEach(e => e.remove());"
        "document.body.classList.remove('modal-open');"
    )


def _nav_click(selenium, xpath):
    _dismiss_modals(selenium)
    element = selenium.find_by_xpath(xpath)
    selenium.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.click()


def _scroll_click(selenium, xpath):
    element = selenium.find_by_xpath(xpath)
    selenium.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    selenium.driver.execute_script("arguments[0].click();", element)


def login_v4_5(selenium, device_user, device_password):
    selenium.open_app()
    selenium.find_by_id("username").send_keys(device_user)
    password = selenium.find_by_id("password")
    password.send_keys(device_password)
    selenium.screenshot('login')
    password.send_keys(Keys.RETURN)
    selenium.find_by_xpath("//h2[contains(.,'Stock overview')]")
    selenium.screenshot('main')


def master_data_v4_5(selenium):
    _nav_click(selenium, "//span[.='Manage master data']")
    selenium.screenshot('master-data')


def locations_v4_5(selenium, count=10):
    _nav_click(selenium, "//span[.='Locations']")
    for i in range(count):
        _dismiss_modals(selenium)
        selenium.find_by_xpath("//a[contains(.,'Add')]").click()
        selenium.driver.switch_to.frame(selenium.find_by_xpath("//iframe"))
        name = f"Location-{i:03d}"
        selenium.click_by(By.ID, "name")
        selenium.find_by_id("name").send_keys(name)
        selenium.find_by_id("description").send_keys(f"{name} description")
        selenium.click_by(By.XPATH, "//button[contains(.,'Save')]")
        selenium.driver.switch_to.default_content()
        selenium.find_by_xpath(f"//td[contains(.,'{name}')]")
    selenium.screenshot('locations')


def products_v4_5(selenium, count=100):
    _nav_click(selenium, "//span[.='Products']")
    for i in range(count):
        selenium.find_by_xpath("//a[contains(.,'Add')]").click()
        product = f"Product-{i:03d}"
        selenium.find_by_id("name").send_keys(product)
        selenium.click_by(By.ID, "location_id")
        selenium.find_by_xpath("//option[.='Fridge']").click()
        selenium.click_by(By.ID, "qu_id_stock")
        selenium.find_by_xpath("//option[.='Pack']").click()
        _scroll_click(selenium, "//button[contains(.,'return to products')]")
        selenium.find_by_xpath("//h2[contains(.,'Products')]")
    selenium.screenshot('products')


def _set_amount(selenium, value, retries=5):
    for _ in range(retries):
        amount_input = selenium.find_by_id("display_amount")
        amount_input.clear()
        amount_input.send_keys(value)
        if amount_input.get_attribute("value") == str(value):
            return
        time.sleep(1)
    raise Exception(f"Failed to set amount to {value}")


def purchase_v4_5(selenium, count=100):
    _nav_click(selenium, "//span[.='Purchase']")
    for i in range(count):
        product = f"Product-{i:03d}"
        _purchase_one_v4_5(selenium, product)
    selenium.screenshot('purchase')


def _purchase_one_v4_5(selenium, product, retries=3):
    for attempt in range(retries):
        selenium.driver.execute_script(
            "document.querySelectorAll('.toast').forEach(e => e.remove());"
        )
        product_input = selenium.find_by_id("product_id_text_input")
        product_input.clear()
        product_input.send_keys(product)
        selenium.find_by_xpath(f"//a[contains(., '{product}')]").click()
        selenium.find_by_xpath(f"//span[@id='productcard-product-name'][contains(.,'{product}')]")
        _set_amount(selenium, 10)
        if selenium.find_by_id("display_amount").get_attribute("value") != "10":
            continue
        today = datetime.today()
        date_input = selenium.find_by_xpath("//div[@id='best_before_date']/input")
        date_input.click()
        date_input.send_keys(Keys.CONTROL + 'a')
        date_input.send_keys(f'{today.year + 1}-01-01')
        date_input.send_keys(Keys.TAB)
        selenium.find_by_id("save-purchase-button").click()
        selenium.find_by_xpath(f"//div[contains(@class,'toast-success')]//div[contains(.,'{product}')]")
        return
    raise Exception(f"Failed to purchase {product} after {retries} attempts")


def stock_overview_v4_5(selenium, expected_products=100):
    _nav_click(selenium, "//span[.='Stock overview']")
    selenium.find_by_xpath(f"//span[contains(., '{expected_products} Products')]")
    selenium.screenshot('stock-overview')


# v4_5 upgrade-only helpers (isolated from UI test)

def products_v4_5_upgrade(selenium, count=100, offset=0):
    _nav_click(selenium, "//span[.='Products']")
    for i in range(count):
        selenium.find_by_xpath("//a[contains(.,'Add')]").click()
        product = f"Product-{offset + i:03d}"
        selenium.find_by_id("name").send_keys(product)
        selenium.click_by(By.ID, "location_id")
        selenium.find_by_xpath("//option[.='Fridge']").click()
        selenium.click_by(By.ID, "qu_id_stock")
        selenium.find_by_xpath("//option[.='Pack']").click()
        _scroll_click(selenium, "//button[contains(.,'return to products')]")
        selenium.find_by_xpath("//h2[contains(.,'Products')]")
    selenium.screenshot('products')


def purchase_v4_5_upgrade(selenium, count=100, offset=0):
    _nav_click(selenium, "//span[.='Purchase']")
    for i in range(count):
        product = f"Product-{offset + i:03d}"
        _purchase_one_v4_5(selenium, product)
    selenium.screenshot('purchase')
