import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ContactsPage(BasePage):
    CONTACT_NAV_LINK = (By.CSS_SELECTOR, "[href = '/contacts']") #CONTACT BUTTON
    CONTACT_CARDS = (By.CLASS_NAME, "contact-item_card__2SOIM")  # CARD
    EDIT_BTN = (By.XPATH, "//button[text()='Edit']")

    EDIT_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Name']")
    EDIT_LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Last Name']")
    EDIT_PHONE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Phone']")
    EDIT_EMAIL_INPUT = (By.CSS_SELECTOR, "input[placeholder='email']")
    EDIT_ADDRESS_INPUT = (By.CSS_SELECTOR, "input[placeholder='Address']")
    EDIT_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "input[placeholder='desc']")

    EDIT_SAVE_BTN = (By.XPATH, "//button[text()='Save']")

    def open_contact_list(self):
        self.click(self.CONTACT_NAV_LINK)
        WebDriverWait(self.driver,5).until(EC.url_contains("/contacts"))
        time.sleep(2)

    def contact_cards_count(self,phone):
        return len(self.driver.find_elements(By.XPATH,f"//h3[text()='{phone}']"))

    # def open_contact_details(self,phone):
    #     card = self.driver.find_element(By.XPATH,f"//h3[text()='{phone}']/...")
    #     card.click()

    def open_contact_details(self,phone):
        locator = (By.XPATH,f"//h3[text()='{phone}']")
        self.click(locator)

    def contact_card_visible(self,phone):
        locator = (By.XPATH,f"//h3[text()='{phone}']")
        element = WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(locator)
        )
        return element.is_displayed()

    def open_edit_mode(self):
        self.click(self.EDIT_BTN)

    def set_edit_field(self, locator, value):
        self.fill(locator,value)

    def submit_edit(self):
        self.click(self.EDIT_SAVE_BTN)
        time.sleep(3)

    def contact_name_for_phone(self,phone):
        card = self.driver.find_element(By.XPATH,f"//h3[text()='{phone}']/..")
        return card.find_element(By.TAG_NAME,"h2").text

    def get_edit_contact(self,locator):
        return self.find(locator).get_attribute("value")
