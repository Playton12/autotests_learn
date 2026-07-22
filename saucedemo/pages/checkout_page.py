import allure
from selenium.webdriver.common.by import By
from saucedemo.pages.base_page import BasePage
from config.settings import UI_BASE_URL


class CheckoutPage(BasePage):
    URL = f"{UI_BASE_URL}/checkout-step-one.html"

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    @allure.step("Open checkout page")
    def open(self) -> None:
        super().open(self.URL)

    @allure.step("Fill checkout info: {first_name} {last_name}")
    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)

    @allure.step("Click continue")
    def click_continue(self) -> None:
        self.click(self.CONTINUE_BUTTON)

    @allure.step("Get error message")
    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)


class CheckoutCompletePage(BasePage):
    URL = f"{UI_BASE_URL}/checkout-complete.html"

    CONFIRMATION_HEADER = (By.CSS_SELECTOR, ".complete-header")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    @allure.step("Get confirmation header text")
    def get_confirmation_header(self) -> str:
        return self.get_text(self.CONFIRMATION_HEADER)

    @allure.step("Click back home")
    def click_back_home(self) -> None:
        self.click(self.BACK_HOME_BUTTON)


class OverviewPage(BasePage):
    FINISH_BUTTON = (By.ID, "finish")
    ITEM_TOTAL = (By.CSS_SELECTOR, ".summary_subtotal_label")

    @allure.step("Click finish")
    def click_finish(self) -> None:
        self.click(self.FINISH_BUTTON)

    @allure.step("Get item total")
    def get_item_total(self) -> str:
        return self.get_text(self.ITEM_TOTAL)
