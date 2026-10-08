import logging
import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class LoginPage(BasePage):

    LOGIN_NAV_LINK = (By.CSS_SELECTOR, "[href='/login']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_BTN = (By.XPATH, "//button[text()='Login']")
    #LOGIN_BTN = (By.XPATH, "//button[text()='LoginBROKEN']")
    SIGN_OUT_BTN = (By.XPATH,"//button[text()='Sign Out']")

    @allure.step("Open login form")
    def open_login_form(self):
        #self.driver.find_element(*self.LOGIN_NAV_LINK).click()
        logger.info("Opening login form")
        self.click(self.LOGIN_NAV_LINK)

    @allure.step("Fill email")
    def fill_email(self,email):
        # self.driver.find_element(*self.EMAIL_INPUT).clear()
        # self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.fill(self.EMAIL_INPUT,email)

    @allure.step("Fill password")
    def fill_password(self,password):
        # self.driver.find_element(*self.PASSWORD_INPUT).clear()
        # self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.fill(self.PASSWORD_INPUT,password)

    @allure.step("Submit login")
    def submit_login(self):
        #self.driver.find_element(*self.LOGIN_BTN).click()
        self.click(self.LOGIN_BTN)

    # def is_logged(self):
    #     try:
    #         self.driver.find_element(*self.SIGN_OUT_BTN)
    #         return True
    #     except NoSuchElementException:
    #         return False

    # def is_logged(self):
    #     try:
    #         WebDriverWait(self.driver, timeout=5).until(
    #             EC.presence_of_element_located(self.SIGN_OUT_BTN)  #visibility of element located
    #         )
    #         return True
    #     except TimeoutException:
    #         return False

    def is_logged(self):
        try:
            self.wait_until_visible(self.SIGN_OUT_BTN)
            return True
        except TimeoutException:
            return False