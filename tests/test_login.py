import logging
import allure
import pytest
from data.user_data import create_user, exiting_user, invalid_email_user, invalid_password_user
from pages.login_page import LoginPage


logger = logging.getLogger(__name__)

# VALID_EMAIL = "anna12345@gmail.com"
# VALID_PASSWORD = "123456!Anna"
#
# INVALID_EMAIL = "anna12345gmail.com"
# INVALID_PASSWORD = "000"

# ----------LOGIN----------
#-------1. Registered user can login with valid data------
# @pytest.mark.smoke
# @pytest.mark.regression
# @allure.feature("Login")
# @allure.story("Login success")
# @allure.title("Logging of user with valid data")
# @allure.description("User with valid data log in the system. Fill fields email and password and click on button [login] ")
# @allure.severity(allure.severity_level.CRITICAL)
def test_login_success(driver):
    login_page = LoginPage(driver)
    user = exiting_user()

    logger.info("Testing successful login: username = %s", user.email)

    login_page.open_login_form()
    login_page.fill_email(user.email)
    login_page.fill_password(user.password)
    login_page.submit_login()
    assert login_page.is_logged() is True

# Negative
#-------2. Registered user can’t login with invalid email and valid password------
@allure.title("Registered user can’t login with invalid email and valid password")
def test_login_wrong_email(driver):
    login_page =LoginPage(driver)
    user = invalid_email_user()
    login_page.open_login_form()
    login_page.fill_email(user.email)
    login_page.fill_password(user.password)
    login_page.submit_login()

    assert login_page.get_alert_text()=="Wrong email or password"
    login_page.accept_alert()

#-------3. Registered user can’t login with valid email and invalid password------
def test_login_wrong_password(driver):
    login_page =LoginPage(driver)
    user = invalid_password_user()
    login_page.open_login_form()
    login_page.fill_email(user.email)
    login_page.fill_password(user.password)
    login_page.submit_login()

    assert login_page.get_alert_text()=="Wrong email or password"
    login_page.accept_alert()

#-------4. Unregistered user can’t login with valid email and valid password------
def test_login_unregistered_user(driver):
    login_page =LoginPage(driver)
    user = create_user(email = "annaAN@gmail.com", password = "Anna123789!")

    login_page.open_login_form()
    login_page.fill_email(user.email)
    login_page.fill_password(user.password)
    login_page.submit_login()

    assert login_page.get_alert_text()=="Wrong email or password"
    login_page.accept_alert()