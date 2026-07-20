import allure
import pytest
from pages.login_page import LoginPage


@allure.feature("Login")
@pytest.mark.ui
@pytest.mark.regression
class TestLoginErrors:
    @allure.title("Login with wrong password shows error")
    def test_wrong_password(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "wrong_password")
        error = login_page.get_error_message()
        assert "Username and password do not match" in error

    @allure.title("Login with locked user shows error")
    def test_locked_user(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("locked_out_user", "secret_sauce")
        error = login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error

    @allure.title("Login with empty username shows error")
    def test_empty_username(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("", "secret_sauce")
        error = login_page.get_error_message()
        assert "Username is required" in error

    @allure.title("Login with empty password shows error")
    def test_empty_password(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "")
        error = login_page.get_error_message()
        assert "Password is required" in error

    @allure.title("Login with empty credentials shows error")
    def test_empty_credentials(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("", "")
        error = login_page.get_error_message()
        assert "Username is required" in error
