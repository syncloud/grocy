import os
from os import environ
from os.path import dirname, join

from selenium import webdriver
from syncloudlib.integration.selenium_wrapper import SeleniumWrapper

from test.ui import test_login, test_master_data, test_products, test_purchase, test_stock_overview

DIR = dirname(__file__)


def test_chrome():

    # sudo docker run -d --name chrome --network ip6net -p 4444:4444 -p 5900:5900 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:4.21.0-20240517
    # firefox http://localhost:7900
    # password: secret

    app_domain = environ["DOMAIN"]
    if app_domain == "":
        raise Exception("DOMAIN env variable is not set")

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    options.set_capability('acceptInsecureCerts', True)
    driver = webdriver.Remote(options=options)
    driver.set_window_rect(0, 0, 1024, 4000)
    driver.maximize_window()
    artifacts_dir = join(DIR, "artifact")
    os.makedirs(artifacts_dir, exist_ok=True )


    selenium = SeleniumWrapper(
        driver,
        "desktop",
        artifacts_dir,
        app_domain,
        30,
        "chrome"
    )

    try:
        test_login(selenium, "test", "test1234")
        test_master_data(selenium)
        # test_products(selenium)
        test_purchase(selenium)
        test_stock_overview(selenium)

    finally:
        print()
        selenium.log()
        driver.quit()
