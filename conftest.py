import datetime
import logging
import re
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from data.contact_data import create_contact
from data.user_data import exiting_user
from pages.add_contact_page import ContactPage
from pages.contacts_page import ContactsPage
from pages.login_page import LoginPage
from tests.test_registration import VALID_EMAIL, VALID_PASSWORD
from utils.logger_config import configure_logging
from utils.selenium_listener import SeleniumEventListener

configure_logging()
logger = logging.getLogger(__name__)
SCREENSHOTS_DIR = Path(__file__).parent/"screenshots"

@pytest.fixture (scope = "function")
def driver():
    logger.info("Starting browser session")
    driver=webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get("https://telranedu.web.app/home")

    yield EventFiringWebDriver(driver,SeleniumEventListener()) #!

    logger.info("Closing browser session")

    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)

@pytest.fixture(autouse=True)
def save_screenshot_on_failure(request,driver):
    yield

    setup_report = getattr(request.node, "rep_setup", None)
    call_report = getattr(request.node, "rep_call", None)
    failed = (setup_report and setup_report.failed) or (call_report and call_report.failed)

    if not failed:
        return

    SCREENSHOTS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_test_name = re.sub(r'[<>:"/\\|?*]', "_", request.node.name)
    filename = f"{safe_test_name}_{timestamp}.png"
    screenshot_path = SCREENSHOTS_DIR / filename

    logger.error("Test failed: %s", request.node.nodeid)
    if driver.save_screenshot(str(screenshot_path)):
        logger.info("Screenshot saved: %s", screenshot_path)

@pytest.fixture
def authenticated_driver(driver):
    login_page = LoginPage(driver)
    user = exiting_user()

    logger.info(f"Logging in user: {user.email}")

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

    count = contacts_page.total_contacts_count()
    if count<3:
        logger.warning(f"Contact list has {count} contacts (<3), creating test data")

    while contacts_page.total_contacts_count()<5:
        contact = create_contact()
        add_contact_page.create_contact_steps(contact)
        contacts_page.open_contact_list()
    return authenticated_driver
