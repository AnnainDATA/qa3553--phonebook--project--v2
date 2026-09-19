import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from tests.test_registration import VALID_EMAIL, VALID_PASSWORD


@pytest.fixture
def driver():
    driver=webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get("https://telranedu.web.app/home")

    yield driver

    driver.quit()

@pytest.fixture
def authenticated_driver(driver):
    login_page = LoginPage(driver)
    login_page.open_login_form()
    login_page.fill_email(VALID_EMAIL)
    login_page.fill_password(VALID_PASSWORD)
    login_page.submit_login()

    return driver