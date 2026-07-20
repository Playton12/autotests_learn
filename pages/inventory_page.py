import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import UI_BASE_URL


class InventoryPage(BasePage):
    URL = f"{UI_BASE_URL}/inventory.html"

    TITLE = (By.CSS_SELECTOR, ".title")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    @allure.step("Open inventory page")
    def open(self) -> None:
        super().open(self.URL)

    @allure.step("Get page title")
    def get_title(self) -> str:
        return self.get_text(self.TITLE)

    @allure.step("Add item to cart by index: {index}")
    def add_item_to_cart(self, index: int) -> None:
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        buttons[index].click()

    @allure.step("Get cart badge count")
    def get_cart_count(self) -> int:
        return int(self.get_text(self.CART_BADGE))
