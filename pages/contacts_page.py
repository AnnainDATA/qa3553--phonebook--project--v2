import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ContactsPage(BasePage):
    CONTACT_NAV_LINK = (By.CSS_SELECTOR, "[href = '/contacts']") #CONTACT BUTTON
    CONTACT_CARDS = (By.CLASS_NAME, "contact-item_card__2SOIM")  # CARD

    def open_contact_list(self):
        self.click(self.CONTACT_NAV_LINK)
        WebDriverWait(self.driver,5).until(EC.url_contains("/contacts"))
        time.sleep(2)

    def contact_cards_count(self,phone):
        return len(self.driver.find_elements(By.XPATH,f"//h3[text()='{phone}']"))

    def open_contact_details(self,phone):
        card = self.driver.find_element(By.XPATH,f"//h3[text()='{phone}']/...")
        card.click()

    def contact_card_visible(self,phone):
        locator = (By.XPATH,f"//h3[text()='{phone}']")
        element = WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(locator)
        )
        return element.is_displayed()