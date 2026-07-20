import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import UI_BASE_URL


class LoginPage(BasePage):
    URL = f"{UI_BASE_URL}/"

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    @allure.step("Open login page")
    def open(self) -> None:
        super().open(self.URL)

    @allure.step("Login as {username}")
    def login(self, username: str, password: str) -> None:
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    @allure.step("Get error message")
    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
