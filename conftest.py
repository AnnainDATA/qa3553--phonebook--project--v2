import logging
import re
from datetime import datetime
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from data.contact_data import create_contact
from data.user_data import exiting_user
from pages.add_contact_page import ContactPage
from pages.contacts_page import ContactsPage
from pages.login_page import LoginPage
from utils.config import BASE_URL
from utils.logger_config import configure_logging
from utils.selenium_listener import SeleniumEventListener

configure_logging()
logger = logging.getLogger(__name__)
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"

#------------------------------------------------------------
def pytest_addoption(parser):
    parser.addoption(   # обьект который пайтест передает в пайтест адопшин
        "--browser",
        action = "store", # сохрани значение как есть по умолчанию, либо что передадим
        default = "chrome", # поумолчанию проэкт гоняется в хроме или том браузере который по дефолту
        choices = ["chrome","firefox","edge"],
        help = "Browser to run tests in: chrome or firefox") # информационная строка

    parser.addoption(
        "--headless", #run the browser without visible window
        action = "store_true", #не ждет значение браузера
        help = "Run the browser without a visible window"
    )
#------------------------------------------------------------

@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser") # обращай внимание что тебе могут передать какой-то браузер
    headless = request.config.getoption("--headless")

    logger.info("Starting browser session")

# выбор браузера на уровне фикстуры драйвер
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    elif browser == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError(f"Unsupported browser:{browser}")


    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get(BASE_URL) #!!!

    yield EventFiringWebDriver(driver, SeleniumEventListener())

    logger.info("Closing browser session")
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


@pytest.fixture(autouse=True)
def save_screenshot_on_failure(request, driver):
    yield

    setup_report = getattr(request.node,"rep_setup",None)
    call_report = getattr(request.node, "rep_call", None)
    failed = (setup_report and setup_report.failed) or(call_report and call_report.failed)

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
        allure.attach.file(
            str(screenshot_path),
            name = "screenshot",
            attachment_type=allure.attachment_type.PNG
        )


@pytest.fixture(scope="function")
def authenticated_driver(driver):
    login_page = LoginPage(driver)
    user = exiting_user()

    logger.info(f"Logging in user: {user.username}")

    login_page.open_login_form()
    login_page.fill_email(user.username)
    login_page.fill_password(user.password)
    login_page.submit_login()

    return driver


@pytest.fixture
def ensure_min_contacts(authenticated_driver):
    contacts_page = ContactsPage(authenticated_driver)
    contact_page = ContactPage(authenticated_driver)

    contacts_page.open_contact_list()

    count = contacts_page.total_contacts_count()
    if count < 3:
        logger.warning(f"Contact list has {count} contacts (<3), creating test data")

    while contacts_page.total_contacts_count() < 3:
        contact_page.create_contact_steps(create_contact())
        contacts_page.open_contact_list()

    return authenticated_driver