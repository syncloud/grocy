import pytest
from subprocess import check_output, run
from syncloudlib.integration.hosts import add_host_alias
from syncloudlib.integration.installer import local_install
from syncloudlib.http import wait_for_rest
import requests

from test import lib

TMP_DIR = '/tmp/syncloud'


@pytest.fixture(scope="session")
def module_setup(request, device, artifact_dir):
    def module_teardown():
        device.run_ssh('journalctl > {0}/refresh.journalctl.log'.format(TMP_DIR), throw=False)
        device.scp_from_device('{0}/*'.format(TMP_DIR), artifact_dir)
        run('cp /videos/* {0}'.format(artifact_dir), shell=True)
        check_output('chmod -R a+r {0}'.format(artifact_dir), shell=True)

    request.addfinalizer(module_teardown)


def test_start(module_setup, app, device_host, domain, device):
    add_host_alias(app, device_host, domain)
    device.activated()
    device.run_ssh('rm -rf {0}'.format(TMP_DIR), throw=False)
    device.run_ssh('mkdir {0}'.format(TMP_DIR), throw=False)


def test_install_stable(device):
    device.run_ssh('snap remove grocy')
    device.run_ssh('snap install grocy', retries=10)


def test_pre_login(selenium, device_user, device_password):
    lib.login_v4_2(selenium, device_user, device_password)


def test_pre_master_data(selenium):
    lib.master_data_v4_2(selenium)


def test_pre_locations(selenium):
    lib.locations_v4_2(selenium, count=10)


def test_pre_products(selenium):
    lib.products_v4_2(selenium, count=10)


def test_pre_purchase(selenium):
    lib.purchase_v4_2(selenium, count=10)


def test_pre_stock_overview(selenium):
    lib.stock_overview_v4_2(selenium, expected_products=10)


def test_upgrade(device, device_password, device_host, app_archive_path, app_domain):
    local_install(device_host, device_password, app_archive_path)
    wait_for_rest(requests.session(), "https://{0}".format(app_domain), 200, 10)


def test_post_login(selenium, device_user, device_password):
    selenium.driver.delete_all_cookies()
    lib.login_v4_5(selenium, device_user, device_password)


def test_post_stock_overview(selenium):
    lib.stock_overview_v4_5(selenium, expected_products=10)


def test_post_master_data(selenium):
    lib.master_data_v4_5(selenium)


def test_post_locations(selenium):
    lib.locations_v4_5(selenium, count=10)


def test_post_products(selenium):
    lib.products_v4_5(selenium, count=10)


def test_post_purchase(selenium):
    lib.purchase_v4_5(selenium, count=10)


def test_post_stock_overview_final(selenium):
    lib.stock_overview_v4_5(selenium, expected_products=20)
