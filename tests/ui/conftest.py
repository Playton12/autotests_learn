import logging
import time

import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from browser_utils import find_browser
from config.settings import BROWSER, HEADLESS, UI_PASSWORD, UI_USERNAME

logger = logging.getLogger(__name__)

_has_browser = find_browser()


def _dismiss_any_dialog(d):
    try:
        for _ in range(3):
            alert = d.switch_to.alert
            alert.accept()
            time.sleep(0.5)
    except Exception:
        pass
    try:
        ActionChains(d).send_keys(Keys.ESCAPE).perform()
        time.sleep(0.3)
        ActionChains(d).send_keys(Keys.ENTER).perform()
        time.sleep(0.3)
    except Exception:
        pass


def _create_chrome_driver(binary: str) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.binary_location = binary
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--incognito")
    options.add_argument(
        "--disable-features=PasswordLeakDetection,PasswordImport,SavePassword,"
        "ChromePasswordManager,InterestFeedContentSuggestions,ChromeWhatsNewUI"
    )
    options.add_argument("--password-store=basic")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("prefs", {
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False,
        "password_manager_enabled": False,
        "safebrowsing.enabled": False,
    })
    return webdriver.Chrome(options=options)


def _create_firefox_driver() -> webdriver.Firefox:
    options = webdriver.FirefoxOptions()
    if HEADLESS:
        options.add_argument("--headless")
    return webdriver.Firefox(options=options)


@pytest.fixture(scope="function")
def driver():
    if not _has_browser:
        pytest.skip("No browser binary found on this machine")

    d = None
    try:
        if BROWSER == "firefox":
            d = _create_firefox_driver()
        else:
            d = _create_chrome_driver(_has_browser)

        d.set_window_size(1920, 1080)
        _dismiss_any_dialog(d)
        yield d
    finally:
        if d is not None:
            try:
                d.quit()
            except Exception:
                pass


@pytest.fixture
def credentials():
    return {"username": UI_USERNAME, "password": UI_PASSWORD}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            try:
                screenshot = driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Screenshot on failure", attachment_type=allure.attachment_type.PNG)
            except (InvalidSessionIdException, WebDriverException):
                logger.warning("Could not capture screenshot: driver session already closed")
