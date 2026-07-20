import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import UI_BASE_URL


class CartPage(BasePage):
    URL = f"{UI_BASE_URL}/cart.html"

    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")

    @allure.step("Open cart page")
    def open(self) -> None:
        super().open(self.URL)

    @allure.step("Get items count in cart")
    def get_items_count(self) -> int:
        return len(self.find_elements(self.CART_ITEMS))

    @allure.step("Click checkout")
    def click_checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)

    @allure.step("Get item names in cart")
    def get_item_names(self) -> list[str]:
        elements = self.find_elements(self.ITEM_NAMES)
        return [el.text for el in elements]
