import allure
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage, OverviewPage, CheckoutCompletePage


@allure.feature("E2E Purchase Flow")
@pytest.mark.ui
@pytest.mark.smoke
class TestE2EPurchase:
    @allure.title("Complete purchase flow: login -> add to cart -> checkout -> finish")
    def test_e2e_purchase(self, driver, credentials):
        with allure.step("Login to the site"):
            login_page = LoginPage(driver)
            login_page.open()
            login_page.login(credentials["username"], credentials["password"])

        with allure.step("Verify inventory page is loaded"):
            inventory_page = InventoryPage(driver)
            assert "Products" in inventory_page.get_title()

        with allure.step("Add first item to cart"):
            inventory_page.add_item_to_cart(0)
            assert inventory_page.get_cart_count() == 1

        with allure.step("Go to cart and verify item"):
            cart_page = CartPage(driver)
            cart_page.open()
            assert cart_page.get_items_count() == 1

        with allure.step("Start checkout"):
            cart_page.click_checkout()

        with allure.step("Fill checkout info"):
            checkout_page = CheckoutPage(driver)
            checkout_page.fill_info("John", "Doe", "12345")
            checkout_page.click_continue()

        with allure.step("Verify overview and finish"):
            overview_page = OverviewPage(driver)
            overview_page.click_finish()

        with allure.step("Verify order confirmation"):
            complete_page = CheckoutCompletePage(driver)
            assert "thank you for your order" in complete_page.get_confirmation_header().lower()


@allure.feature("E2E Purchase Flow")
@pytest.mark.ui
@pytest.mark.regression
class TestCheckoutErrors:
    @allure.title("Checkout with empty fields shows error")
    def test_checkout_empty_fields(self, driver, credentials):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(credentials["username"], credentials["password"])

        cart_page = CartPage(driver)
        cart_page.open()
        cart_page.click_checkout()

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_info("", "", "")
        checkout_page.click_continue()
        error = checkout_page.get_error_message()
        assert "Error" in error

    @allure.title("Add multiple items to cart")
    def test_add_multiple_items(self, driver, credentials):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(credentials["username"], credentials["password"])

        inventory_page = InventoryPage(driver)
        assert "Products" in inventory_page.get_title()

        inventory_page.add_item_to_cart(0)
        inventory_page.add_item_to_cart(1)
        inventory_page.add_item_to_cart(2)
        assert inventory_page.get_cart_count() == 3

        cart_page = CartPage(driver)
        cart_page.open()
        assert cart_page.get_items_count() == 3
