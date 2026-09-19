#pytest -v tests/test_login.py
from pages.login_page import LoginPage
from models.user import User

# ----------LOGIN----------
#-------1. Registered user can login with valid data------
def test_login_success(driver):
    login_page = LoginPage(driver)
    user = User(
        "anna12345@gmail.com",
        "123456!Anna"
    )
    login_page.open_login_form()
    login_page.fill_email(user.email)
    login_page.fill_password(user.password)
    login_page.submit_login()

    assert login_page.is_logged() is True

# Negative
#-------2. Registered user can’t login with invalid email and valid password------
def test_login_wrong_email(driver):
    login_page =LoginPage(driver)
    user = User(
        "anna12345gmail.com",
        "123456!Anna"
    )
    login_page.open_login_form()
    login_page.fill_email(user.email)
    login_page.fill_password(user.password)
    login_page.submit_login()

    assert login_page.get_alert_text()=="Wrong email or password"
    login_page.accept_alert()

#-------3. Registered user can’t login with valid email and invalid password------
def test_login_wrong_password(driver):
    login_page =LoginPage(driver)
    user = User(
        "anna12345@gmail.com",
        "2222"
    )
    login_page.open_login_form()
    login_page.fill_email(user.email)
    login_page.fill_password(user.password)
    login_page.submit_login()

    assert login_page.get_alert_text()=="Wrong email or password"
    login_page.accept_alert()

#-------4. Unregistered user can’t login with valid email and valid password------
def test_login_unregistered_user(driver):
    login_page =LoginPage(driver)

    login_page.open_login_form()
    login_page.fill_email("annaAN@gmail.com")
    login_page.fill_password("Anna123789!")
    login_page.submit_login()

    assert login_page.get_alert_text()=="Wrong email or password"
    login_page.accept_alert()