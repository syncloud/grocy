from os.path import dirname, join
from subprocess import check_output

import pytest
from syncloudlib.integration.hosts import add_host_alias

from lib import login_v4_5, master_data_v4_5, locations_v4_5, products_v4_5, purchase_v4_5, stock_overview_v4_5

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
    login_v4_5(selenium, device_user, device_password)


def test_master_data(selenium):
    master_data_v4_5(selenium)


def test_locations(selenium):
    locations_v4_5(selenium)


def test_products(selenium):
    products_v4_5(selenium)


def test_purchase(selenium):
    purchase_v4_5(selenium)


def test_stock_overview(selenium):
    stock_overview_v4_5(selenium)
