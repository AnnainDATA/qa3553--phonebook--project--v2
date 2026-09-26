import logging

import pytest
from selenium import webdriver
from data.contact_data import create_contact
from data.user_data import exiting_user
from pages.add_contact_page import ContactPage
from pages.contacts_page import ContactsPage
from pages.login_page import LoginPage
from tests.test_registration import VALID_EMAIL, VALID_PASSWORD
from utils.logger_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

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
    user = exiting_user()
    login_page.open_login_form()
    login_page.fill_email(user.email)
    login_page.fill_password(user.password)
    login_page.submit_login()

    return driver

#fixture for preparing contacts to be deleted
@pytest.fixture
def ensure_min_contacts(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contacts_page.open_contact_list()
    while contacts_page.total_contacts_count()<5:
        contact = create_contact()
        add_contact_page.create_contact_steps(contact)
        contacts_page.open_contact_list()
    return authenticated_driver
