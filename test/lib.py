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
        selenium.find_by_xpath("//a[contains(.,'Add')]").click()
        selenium.driver.switch_to.frame(selenium.find_by_xpath("//iframe"))
        name = f"Location-{i:03d}"
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
        selenium.find_by_xpath("//button[contains(.,'return to products')]").click()
    selenium.screenshot('products')


def purchase_v4_2(selenium, count=100):
    selenium.find_by_xpath("//span[.='Purchase']").click()
    for i in range(count):
        product = f"Product-{i:03d}"
        selenium.find_by_id("product_id_text_input").send_keys(product)
        selenium.find_by_xpath(f"//a[contains(., '{product}')]").click()
        selenium.find_by_id("display_amount").send_keys(10)
        selenium.find_by_css(".fa-calendar").click()
        today = datetime.today()
        selenium.find_by_xpath("//div[@id='best_before_date']/input").send_keys(f'{today.year + 1}-1-1')
        selenium.find_by_id("save-purchase-button").click()
    selenium.screenshot('purchase')


def stock_overview_v4_2(selenium, expected_products=100):
    selenium.find_by_xpath("//span[.='Stock overview']").click()
    selenium.find_by_xpath(f"//span[contains(., '{expected_products} Products')]")
    selenium.screenshot('stock-overview')


# v4_5 helpers (current grocy UI)

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
    selenium.find_by_xpath("//span[.='Manage master data']").click()
    selenium.screenshot('master-data')


def locations_v4_5(selenium, count=10):
    selenium.find_by_xpath("//span[.='Locations']").click()
    for i in range(count):
        selenium.find_by_xpath("//a[contains(.,'Add')]").click()
        selenium.driver.switch_to.frame(selenium.find_by_xpath("//iframe"))
        name = f"Location-{i:03d}"
        selenium.find_by_id("name").send_keys(name)
        selenium.find_by_id("description").send_keys(f"{name} description")
        selenium.click_by(By.XPATH, "//button[contains(.,'Save')]")
        selenium.driver.switch_to.default_content()
        selenium.find_by_xpath(f"//td[contains(.,'{name}')]")
    selenium.screenshot('locations')


def products_v4_5(selenium, count=100):
    selenium.find_by_xpath("//span[.='Products']").click()
    for i in range(count):
        selenium.find_by_xpath("//a[contains(.,'Add')]").click()
        product = f"Product-{i:03d}"
        selenium.find_by_id("name").send_keys(product)
        selenium.click_by(By.ID, "location_id")
        selenium.find_by_xpath("//option[.='Fridge']").click()
        selenium.click_by(By.ID, "qu_id_stock")
        selenium.find_by_xpath("//option[.='Pack']").click()
        selenium.find_by_xpath("//button[contains(.,'return to products')]").click()
    selenium.screenshot('products')


def purchase_v4_5(selenium, count=100):
    selenium.find_by_xpath("//span[.='Purchase']").click()
    for i in range(count):
        product = f"Product-{i:03d}"
        selenium.find_by_id("product_id_text_input").send_keys(product)
        selenium.find_by_xpath(f"//a[contains(., '{product}')]").click()
        selenium.find_by_id("display_amount").send_keys(10)
        selenium.find_by_css(".fa-calendar").click()
        today = datetime.today()
        selenium.find_by_xpath("//div[@id='best_before_date']/input").send_keys(f'{today.year + 1}-1-1')
        selenium.find_by_id("save-purchase-button").click()
    selenium.screenshot('purchase')


def stock_overview_v4_5(selenium, expected_products=100):
    selenium.find_by_xpath("//span[.='Stock overview']").click()
    selenium.find_by_xpath(f"//span[contains(., '{expected_products} Products')]")
    selenium.screenshot('stock-overview')
