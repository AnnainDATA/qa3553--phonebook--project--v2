from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self,driver):
        self.driver = driver

    def find(self,locator):
        return self.driver.find_element(*locator)

    def click(self,locator):
        return self.find(locator).click()

    def fill(self,locator,value):
        self.find(locator).clear()
        self.find(locator).send_keys(value)

#------for alert------
    def get_alert_text(self):
        alert=WebDriverWait(self.driver,timeout=5).until(
            EC.alert_is_present()
        )
        return alert.text

    def accept_alert(self):
        self.driver.switch_to.alert.accept()