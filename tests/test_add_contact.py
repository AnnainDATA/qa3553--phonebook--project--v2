#pytest -v tests/test_add_contact.py
import pytest
import logging
from faker import Faker

from data.contact_data import create_contact
from data.contact_datasets import PHONE_ALERT_TEXT, EMAIL_ALERT_TEXT
from models.contact import Contact
from pages.add_contact_page import ContactPage
from pages.contacts_page import ContactsPage

fake = Faker()
logger = logging.getLogger(__name__)

#------POSITIVE------
#------Successfully creating new contact with valid data------
def test_add_contact_success_all_fields(authenticated_driver):
    logger.info("Test: test_add_contact_success_all_fields")
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact()
    add_contact_page.create_contact_steps(contact)
    assert contacts_page.contact_card_visible(contact.phone)

def test_add_contact_success_required_fields(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact(description="")
    add_contact_page.create_contact_steps(contact)
    assert contacts_page.contact_card_visible(contact.phone)

#------NEGATIVE------
def test_add_contact_empty_name(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact(name="")

    add_contact_page.open_contact_form()
    add_contact_page.fill_contact(contact)
    add_contact_page.submit_contact()

    assert add_contact_page.is_add_button_active()
    contacts_page.open_contact_list()
    assert contacts_page.contact_cards_count(contact.phone) == 0

def test_add_contact_empty_last_name(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact(last_name="")

    # add_contact_page.open_contact_form()
    # add_contact_page.fill_contact(contact)
    # add_contact_page.submit_contact()

    add_contact_page.create_contact_steps(contact)
    assert add_contact_page.is_add_button_active()
    contacts_page.open_contact_list()
    assert contacts_page.contact_cards_count(contact.phone) == 0

#@pytest.mark.skip (reason = "Contact with empty email")
@pytest.mark.xfail (reason = "Contact with empty email")
def test_add_contact_empty_email(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact(email="")
    add_contact_page.create_contact_steps(contact)

    assert add_contact_page.is_add_button_active()
    contacts_page.open_contact_list()
    assert contacts_page.contact_cards_count(contact.phone) == 0

def test_add_contact_empty_address(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact(address="")
    add_contact_page.create_contact_steps(contact)

    assert add_contact_page.is_add_button_active()
    contacts_page.open_contact_list()
    assert contacts_page.contact_cards_count(contact.phone) == 0


@pytest.mark.parametrize(
    "phone",
    ["055898",
     "05589899991111222225555",
     "#0558989999",
     "helloworld",
     "055898hello",
     "hello055898",
     "055898world88",
     "##!!@@##^^",
     "0558985566##",
     "##0558985566",
     "055898$$5566",
     "0558988899 0558986655"
     "0558988899,0558986655",
     "          ",
     "",
     "  0558988899",
     "0558988899   ",
     "055898   8899"
     ]
)
def test_add_contact_invalid_phone(authenticated_driver,phone):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact(phone=phone)
    add_contact_page.create_contact_steps(contact)

    assert add_contact_page.get_alert_text().strip() == PHONE_ALERT_TEXT
    add_contact_page.accept_alert()
    assert add_contact_page.is_add_button_active()
    contacts_page.open_contact_list()
    assert contacts_page.contact_cards_count(contact.phone) == 0

@pytest.mark.parametrize(
    "field, value, expected_alert",
        [
        ("email","",EMAIL_ALERT_TEXT),
        ("email","simon@@gmail.com",EMAIL_ALERT_TEXT),
        ("email","simongmail.com",EMAIL_ALERT_TEXT),
        ("email","simon@gmail",EMAIL_ALERT_TEXT),
        ("email","simon1@",EMAIL_ALERT_TEXT),
        ("email","simonsimonsimonsimonsimonsimonsimonsimon@gmail.com",EMAIL_ALERT_TEXT),
        ("email","simon@gmailgmail.com",EMAIL_ALERT_TEXT),
        ("email","s@g",EMAIL_ALERT_TEXT),
        ("email","gmail.com@סימון",EMAIL_ALERT_TEXT),
        ("email","  simon@gmail.com",EMAIL_ALERT_TEXT),
("email","simon@gmail.com   ",EMAIL_ALERT_TEXT),
("email","##@gmail.com",EMAIL_ALERT_TEXT),
("email","%%!!@gmail.com",EMAIL_ALERT_TEXT),
("email","simon@gmail.com simon@gmail.com",EMAIL_ALERT_TEXT),
("email","simon@gmail.comsimon@gmail.com",EMAIL_ALERT_TEXT)
         ]
)
def test_add_contact_invalid_email(authenticated_driver,field,value,expected_alert):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact(**{field:value})
    add_contact_page.create_contact_steps(contact)

    assert add_contact_page.get_alert_text().strip() == EMAIL_ALERT_TEXT
    add_contact_page.accept_alert()
    assert add_contact_page.is_add_button_active()
    contacts_page.open_contact_list()
    assert contacts_page.contact_cards_count(contact.phone) == 0

@pytest.mark.xfail (reason = "Contact with duplicate phone")
def test_add_contact_duplicate_phone_rejected(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    shared_phone = fake.unique.numerify("050########")

    first_contact = create_contact(phone = shared_phone)
    second_contact = create_contact(phone=shared_phone)

    add_contact_page.create_contact_steps(first_contact)
    assert contacts_page.contact_card_visible(shared_phone)

    add_contact_page.create_contact_steps(second_contact)
    contacts_page.open_contact_list()
    assert contacts_page.contact_cards_count(shared_phone) == 1



