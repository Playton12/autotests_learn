import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import WAIT_TIMEOUT


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_TIMEOUT)

    @allure.step("Open URL: {url}")
    def open(self, url: str) -> None:
        self.driver.get(url)

    @allure.step("Find element: {locator}")
    def find(self, locator: tuple) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Find elements: {locator}")
    def find_elements(self, locator: tuple) -> list[WebElement]:
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    @allure.step("Click element: {locator}")
    def click(self, locator: tuple) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    @allure.step("Type text into: {locator}")
    def type_text(self, locator: tuple, text: str) -> None:
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Get text from: {locator}")
    def get_text(self, locator: tuple) -> str:
        return self.find(locator).text
