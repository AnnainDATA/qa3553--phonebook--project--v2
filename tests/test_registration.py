#pytest -v tests/test_registration.py
import time
from pages.registration_page import RegistrationPage
from models.user import User

VALID_EMAIL="anna12345@gmail.com"
VALID_PASSWORD="123456!Anna"

# --------Valid unique email generator
def generate_unique_email():
    timestamp = int(time.time() * 1000)
    return f"user_{timestamp}@gmail.com"

# Positive
#-------1. Unregistered user can register with valid data------
def test_registration_success(driver):
    registration_page = RegistrationPage(driver)
    user = User(
        generate_unique_email(),
        "123456!Anna"
    )
    registration_page.open_registration_form()
    registration_page.fill_email(user.email)
    registration_page.fill_password(user.password)
    registration_page.submit_registration()

    assert registration_page.is_registered() is True

# Negative
#-------2. Unregistered user can`t register with invalid email and valid password------
def test_registration_wrong_email(driver):
    registration_page = RegistrationPage(driver)
    user = User(
        generate_unique_email(),
        "123456!Anna"
    )
    registration_page.open_registration_form()
    registration_page.fill_email(f" {user.email}") #space before email
    registration_page.fill_password(user.password)
    registration_page.submit_registration()

    assert "Wrong email or password format" in registration_page.get_alert_text()
    registration_page.accept_alert()

#-------3. Unregistered user can`t register with valid email and invalid password------
def test_registration_wrong_password(driver):
    registration_page = RegistrationPage(driver)
    user = User(
        generate_unique_email(),
        "000"
    )
    registration_page.open_registration_form()
    registration_page.fill_email(user.email)
    registration_page.fill_password(user.password)
    registration_page.submit_registration()

    assert "Wrong email or password format" in registration_page.get_alert_text()
    registration_page.accept_alert()

#-------4. Registered user can`t register with registered data (email and password)------
def test_registration_exists_user(driver):
    registration_page = RegistrationPage(driver)

    registration_page.open_registration_form()
    registration_page.fill_email(VALID_EMAIL)
    registration_page.fill_password(VALID_PASSWORD)
    registration_page.submit_registration()
    time.sleep(2)
    assert registration_page.get_alert_text() == "User already exist"
    registration_page.accept_alert()

#-------5. Registered user can`t register with registered email and new valid password------
def test_registration_valid_pwd_registered_email(driver):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_form()
    registration_page.fill_email(VALID_EMAIL)
    registration_page.fill_password("AnnaAnna77!")
    registration_page.submit_registration()

    alert_text=registration_page.get_alert_text()
    assert "User already exist" in alert_text

    assert registration_page.get_alert_text()=="User already exist"
    registration_page.accept_alert()