from os.path import dirname, join
from subprocess import check_output
from selenium.webdriver.common.by import By
from datetime import datetime

import pytest
from selenium.webdriver.common.keys import Keys
from syncloudlib.integration.hosts import add_host_alias

DIR = dirname(__file__)
TMP_DIR = '/tmp/syncloud/ui'


@pytest.fixture(scope="session")
def module_setup(request, selenium, device, artifact_dir, ui_mode):
    def module_teardown():
        device.activated()
        device.run_ssh('mkdir -p {0}'.format(TMP_DIR), throw=False)
        device.run_ssh('journalctl > {0}/journalctl.ui.{1}.log'.format(TMP_DIR, ui_mode), throw=False)
        device.run_ssh('cp /var/log/syslog {0}/syslog.ui.{1}.log'.format(TMP_DIR, ui_mode), throw=False)
        device.scp_from_device('{0}/*'.format(TMP_DIR), join(artifact_dir, 'log'))
        check_output('cp /videos/* {0}'.format(artifact_dir), shell=True)
        check_output('chmod -R a+r {0}'.format(artifact_dir), shell=True)
        selenium.log()
        
    request.addfinalizer(module_teardown)


def test_start(module_setup, app, domain, device_host):
    add_host_alias(app, device_host, domain)


def test_login(selenium, device_user, device_password):
    selenium.open_app()
    selenium.find_by_id("username").send_keys(device_user)
    password = selenium.find_by_id("password")
    password.send_keys(device_password)
    selenium.screenshot('login')
    password.send_keys(Keys.RETURN)
    selenium.find_by_xpath("//h2[contains(.,'Stock overview')]")
    selenium.screenshot('main')


def test_master_data(selenium):
    selenium.find_by_xpath("//span[.='Manage master data']").click()
    selenium.screenshot('master-data')


def test_locations(selenium):
    selenium.find_by_xpath("//span[.='Locations']").click()
    for i in range(10):
        selenium.find_by_xpath("//a[contains(.,'Add')]").click()
        selenium.driver.switch_to.frame(selenium.find_by_xpath("//iframe"))
        name = f"Location-{i:03d}"
        selenium.find_by_id("name").send_keys(name)
        selenium.find_by_id("description").send_keys(f"{name} description")
        selenium.click_by(By.XPATH, "//button[contains(.,'Save')]")
        selenium.driver.switch_to.default_content()
        selenium.find_by_xpath(f"//td[contains(.,'{name}')]")
    selenium.screenshot('locations')


def test_products(selenium):
    selenium.find_by_xpath("//span[.='Products']").click()
    for i in range(100):
        selenium.find_by_xpath("//a[contains(.,'Add')]").click()
        product = f"Product-{i:03d}"
        selenium.find_by_id("name").send_keys(product)
        selenium.click_by(By.ID, "location_id")
        selenium.find_by_xpath("//option[.='Fridge']").click()
        selenium.click_by(By.ID, "qu_id_stock")
        selenium.find_by_xpath("//option[.='Pack']").click()
        selenium.find_by_xpath("//button[contains(.,'return to products')]").click()
    selenium.screenshot('products')


def test_purchase(selenium):
    selenium.find_by_xpath("//span[.='Purchase']").click()
    for i in range(100):
        product = f"Product-{i:03d}"
        selenium.find_by_id("product_id_text_input").send_keys(product)
        selenium.find_by_xpath(f"//a[contains(., '{product}')]").click()
        selenium.find_by_id("display_amount").send_keys(10)
        selenium.find_by_css(".fa-calendar").click()
        today = datetime.today()
        selenium.find_by_xpath("//div[@id='best_before_date']/input").send_keys(f'{today.year + 1}-1-1')
        selenium.find_by_id("save-purchase-button").click()
    selenium.screenshot('purchase')

def test_stock_overview(selenium):
    selenium.find_by_xpath("//span[.='Stock overview']").click()
    selenium.find_by_xpath("//span[contains(., '100 Products')]")
    selenium.screenshot('stock-overview')
