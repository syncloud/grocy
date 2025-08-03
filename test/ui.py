from os.path import dirname, join
from subprocess import check_output
from selenium.webdriver.common.by import By

import pytest
from selenium.webdriver.common.keys import Keys
from syncloudlib.integration.hosts import add_host_alias

DIR = dirname(__file__)
TMP_DIR = '/tmp/syncloud/ui'


@pytest.fixture(scope="session")
def module_setup(request, device, artifact_dir, ui_mode):
    def module_teardown():
        device.activated()
        device.run_ssh('mkdir -p {0}'.format(TMP_DIR), throw=False)
        device.run_ssh('journalctl > {0}/journalctl.ui.{1}.log'.format(TMP_DIR, ui_mode), throw=False)
        device.run_ssh('cp /var/log/syslog {0}/syslog.ui.{1}.log'.format(TMP_DIR, ui_mode), throw=False)
        device.scp_from_device('{0}/*'.format(TMP_DIR), join(artifact_dir, 'log'))
        check_output('chmod -R a+r {0}'.format(artifact_dir), shell=True)

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


def test_master_data(selenium, device_user, device_password):
    selenium.find_by_xpath("//span[.='Manage master data']").click()
    selenium.screenshot('master-data')


def test_locations(selenium, device_user, device_password):
    selenium.find_by_xpath("//span[.='Locations']").click()
    for i in range(10):
        selenium.find_by_xpath("//a[contains(.,'Add')]").click()
        selenium.driver.switch_to.frame(selenium.find_by_xpath("//iframe"))
        name = 'Location-' + str(i)
        selenium.find_by_id("name").send_keys(name)
        selenium.click_by(By.XPATH, "//button[contains(.,'Save')]")
        selenium.driver.switch_to.default_content()
        selenium.find_by_xpath(f"//td[contains(.,'{name}')]")
    selenium.screenshot('locations')


def test_products(selenium, device_user, device_password):
    selenium.find_by_xpath("//span[.='Products']").click()
    for i in range(100):
        selenium.find_by_xpath("//a[contains(.,'Add')]").click()
        selenium.find_by_id("name").send_keys('Product-' + str(i))
        selenium.find_by_id("location_id").click()
        selenium.find_by_xpath("//option[.='Fridge')]").click()
        selenium.find_by_id("qu_id_stock").click()
        selenium.find_by_xpath("//option[.='Pack')]").click()
        selenium.find_by_xpath("//button[contains(.,'return to products')]").click()
    selenium.screenshot('products')

