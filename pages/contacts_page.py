import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class ContactsPage(BasePage):
    CONTACT_NAV_LINK = (By.CSS_SELECTOR, "[href = '/contacts']") #CONTACT BUTTON
    CONTACT_CARDS = (By.CLASS_NAME, "contact-item_card__2SOIM")  # CARD
    EDIT_BTN = (By.XPATH, "//button[text()='Edit']")
    REMOVE_BTN = (By.XPATH, "//button[text()='Remove']") #REMOVE BUTTON

    EDIT_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Name']")
    EDIT_LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Last Name']")
    EDIT_PHONE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Phone']")
    EDIT_EMAIL_INPUT = (By.CSS_SELECTOR, "input[placeholder='email']")
    EDIT_ADDRESS_INPUT = (By.CSS_SELECTOR, "input[placeholder='Address']")
    EDIT_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "input[placeholder='desc']")
    EDIT_SAVE_BTN = (By.XPATH, "//button[text()='Save']")

    def open_contact_list(self):
        self.click(self.CONTACT_NAV_LINK)
        self.wait_until_url_matches(r"/contacts$")

    def contact_cards_count(self,phone):
        return len(self.driver.find_elements(By.XPATH,f"//h3[text()='{phone}']"))

    # def open_contact_details(self,phone):
    #     card = self.driver.find_element(By.XPATH,f"//h3[text()='{phone}']/...")
    #     card.click()

    def open_contact_details(self,phone):
        logger.info(f"Opening contact details for phone{phone}")
        locator = (By.XPATH,f"//h3[text()='{phone}']")
        self.click(locator)

    def contact_card_visible(self,phone):
        locator = (By.XPATH,f"//h3[text()='{phone}']")
        return self.wait_until_visible(locator).is_displayed()

    def open_edit_mode(self):
        logger.info(f"Opening edit mode")
        self.click(self.EDIT_BTN)

    def set_edit_field(self, locator, value):
        self.fill(locator,value)

    def submit_edit(self):
        logger.info("Submitting contact edit")
        self.click(self.EDIT_SAVE_BTN)
        time.sleep(3)

    def contact_name_for_phone(self,phone):
        card = self.driver.find_element(By.XPATH,f"//h3[text()='{phone}']/..")
        return card.find_element(By.TAG_NAME,"h2").text

    def get_edit_contact(self,locator):
        return self.find(locator).get_attribute("value")

    def remove_contact(self):
        logger.info("Deleting contact")
        self.click(self.REMOVE_BTN)
        self.wait_until_url_matches(r"/contacts$")

    def all_contact_cards_count(self):
        return len(self.driver.find_elements(By.CLASS_NAME, "contact-item_card__2SOIM"))

    def open_first_contact(self):
        cards = self.driver.find_elements(*self.CONTACT_CARDS)
        first_card = cards[0]
        first_card.click()

    def total_contacts_count(self):
        return len(self.driver.find_elements(*self.CONTACT_CARDS))

    def delete_all_contacts(self):
        logger.info("Deleting all contacts")
        while self.total_contacts_count() > 0:
            self.open_first_contact()
            self.remove_contact()
