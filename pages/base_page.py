from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self,driver):
        self.driver = driver

    def find(self,locator):
        return self.driver.find_element(*locator)

    def click(self,locator):
        self.wait_until_clickable(locator).click()

    def fill(self,locator,value):
        element = self.wait_until_visible(locator)
        element.clear()
        element.send_keys(value)
        # self.find(locator).clear()
        # self.find(locator).send_keys(value)

#------methods for alert------
    def get_alert_text(self):
        return self.wait_until_alert_present().text

    def accept_alert(self):
        self.driver.switch_to.alert.accept()

# --WAIT UNTIL--
    def wait_until_visible(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator))   #visibility of element located not working

    def wait_until_clickable(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator))

    def wait_until_url_matches(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.url_matches(locator))

    def wait_until_alert_present(self, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.alert_is_present())
