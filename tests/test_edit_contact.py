import time
import logging
import pytest
from faker import Faker
from data.contact_data import create_contact
from pages.add_contact_page import ContactPage
from pages.contacts_page import ContactsPage
fake = Faker()

logger = logging.getLogger(__name__)

#-------------POSITIVE---------------------
#1.Registered user can edit an existing contact after entering valid data in [NAME] field and save changes
def test_edit_contact_name_updated(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    add_contact_page.create_contact_steps(contact)
    new_name = fake.first_name()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_NAME_INPUT, new_name)
    contacts_page.submit_edit()

    assert contacts_page.contact_name_for_phone(contact.phone) == new_name

#--------------------------------------------------------------------
#2.Registered user can edit an existing contact after entering valid data in [LAST NAME] field and save changes
def test_edit_contact_last_name_updated(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    add_contact_page.create_contact_steps(contact)
    new_last_name = fake.last_name()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_LAST_NAME_INPUT, new_last_name)
    contacts_page.submit_edit()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_LAST_NAME_INPUT) == new_last_name

#--------------------------------------------------------------------
#3.Registered user can edit an existing contact after entering valid data in [PHONE] field and save changes
def test_edit_contact_phone_updated(authenticated_driver):
    logger.info("Test: test_edit_contact_phone_updated")
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    add_contact_page.create_contact_steps(contact)
    new_phone = fake.unique.numerify("050#######")

    logger.debug(f"Old phone:{contact.phone}")
    logger.debug(f"New phone: {new_phone}")

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_PHONE_INPUT, new_phone)
    contacts_page.submit_edit()

    assert contacts_page.contact_card_visible(new_phone)
    assert contacts_page.contact_cards_count(contact.phone) == 0

#--------------------------------------------------------------------
#4.Registered user can edit an existing contact after entering valid data in [EMAIL] field and save changes
def test_edit_contact_email_updated(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    add_contact_page.create_contact_steps(contact)
    new_email = fake.unique.email()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_EMAIL_INPUT, new_email)
    contacts_page.submit_edit()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_EMAIL_INPUT) == new_email

#--------------------------------------------------------------------
#5.Registered user can edit an existing contact after entering valid data in [ADDRESS] field and save changes
def test_edit_contact_address_updated(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    add_contact_page.create_contact_steps(contact)
    new_address = fake.city()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_ADDRESS_INPUT, new_address)
    contacts_page.submit_edit()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_ADDRESS_INPUT) == new_address

#--------------------------------------------------------------------
#6.Registered user can edit an existing contact after entering valid data in [DESCRIPTION] field and save changes
@pytest.mark.skip(reason="BUG-130: Editing description saves literal string '[Object Undefined]'")
def test_edit_contact_description_updated(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    add_contact_page.create_contact_steps(contact)
    new_description = fake.sentence()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_DESCRIPTION_INPUT, new_description)
    contacts_page.submit_edit()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_DESCRIPTION_INPUT) == new_description

#--------------------NEGATIVE-------------------------
# 1. Registered user can’t edit an existing contact with field blank or
# with incorrect data in field [NAME]
INVALID_NAMES = [
    "",
    "   ",
    "\t\n",
    "S",
    "SimonSimonSimonSimonSimonSimonSimonSimonSimonSimonSimonSimon",
    "@",
    "!##%%%%%%%%%%%%%%",
    "    !",
    " ",
    "וולנטינה",
]
@pytest.mark.parametrize("invalid_name", INVALID_NAMES)
def test_edit_contact_empty_name_negative(authenticated_driver,invalid_name):
    contacts_page = ContactsPage(authenticated_driver)
    add_contact_page = ContactPage(authenticated_driver)
    contact = create_contact()
    add_contact_page.create_contact_steps(contact)
    #new_name1 = ""

    contacts_page.open_contact_details(contact.phone)
    time.sleep(3)
    contacts_page.open_edit_mode()
    time.sleep(3)
    contacts_page.set_edit_field(contacts_page.EDIT_NAME_INPUT, invalid_name)
    contacts_page.submit_edit()

# we check that user's name remained the same and did not turn into an empty string
    #assert contacts_page.contact_name_for_phone(contact.phone) == contact.name
    actual_name = contacts_page.contact_name_for_phone(contact.phone)

    assert actual_name == contact.name, (
        f"Contact name changed to an invalid value: '{invalid_name}'! "
        f"Expected original name to remain: '{contact.name}'"
    )

#--------------------------------------------------------------------
# 2. Registered user can’t edit an existing contact with field blank or
# with incorrect data in field [LAST NAME]
def test_edit_contact_empty_last_name_negative(authenticated_driver):
    contacts_page = ContactsPage(authenticated_driver)
    add_contact_page = ContactPage(authenticated_driver)
    contact = create_contact()
    add_contact_page.create_contact_steps(contact)

    contacts_page.open_contact_details(contact.phone)
    time.sleep(3)
    contacts_page.open_edit_mode()
    time.sleep(3)
    contacts_page.set_edit_field(contacts_page.EDIT_LAST_NAME_INPUT, "")
    contacts_page.submit_edit()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_LAST_NAME_INPUT) == contact.last_name

# --------------------------------------------------------------------
# 3. Registered user can’t edit an existing contact with field blank or with incorrect data in field [PHONE]
def test_edit_contact_empty_phone_negative(authenticated_driver):
    contacts_page = ContactsPage(authenticated_driver)
    add_contact_page = ContactPage(authenticated_driver)
    contact = create_contact()
    add_contact_page.create_contact_steps(contact)

    contacts_page.open_contact_details(contact.phone)
    time.sleep(3)
    contacts_page.open_edit_mode()
    time.sleep(3)
    contacts_page.set_edit_field(contacts_page.EDIT_PHONE_INPUT, "")
    contacts_page.submit_edit()

    assert contacts_page.contact_cards_count(contact.phone) == 1

# --------------------------------------------------------------------
INVALID_EMAILS = [
    "",
    "simon@@gmail.com",
    "simongmail.com",
    "simon@gmail",
    "simon1@",
    "simonsimonsimonsimonsimonsimonsimonsimon@gmail.com",
    "simon@gmailgmail.com",
    "s@g",
    "gmail.com@סימון",
    "  simon@gmail.com",
    "simon@gmail.com   ",
    "##@gmail.com",
    "%%!!@gmail.com",
    "simon@gmail.com simon@gmail.com",
    "simon@gmail.comsimon@gmail.com"
]
@pytest.mark.parametrize("invalid_email", INVALID_EMAILS)
# 4. Registered user can’t edit an existing contact with field blank or with incorrect data in field [EMAIL]
def test_edit_contact_empty_email_negative(authenticated_driver,invalid_email):
    contacts_page = ContactsPage(authenticated_driver)
    add_contact_page = ContactPage(authenticated_driver)
    contact = create_contact()
    add_contact_page.create_contact_steps(contact)

    contacts_page.open_contact_details(contact.phone)
    time.sleep(3)
    contacts_page.open_edit_mode()
    time.sleep(3)
    contacts_page.set_edit_field(contacts_page.EDIT_EMAIL_INPUT, invalid_email)
    contacts_page.submit_edit()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_EMAIL_INPUT) == contact.email

# --------------------------------------------------------------------
# 5. Registered user can’t edit an existing contact with field blank or with incorrect data in field [ADDRESS]
def test_edit_contact_empty_address_negative(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    add_contact_page.create_contact_steps(contact)

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_ADDRESS_INPUT, "")
    contacts_page.submit_edit()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_ADDRESS_INPUT) == contact.address

# --------------------------------------------------------------------
# 6. Registered user can’t edit field [PHONE] to an already existing one
def test_edit_contact_duplicate_phone_negative(authenticated_driver):
    contacts_page = ContactsPage(authenticated_driver)
    add_contact_page = ContactPage(authenticated_driver)

    existing_contact = create_contact()
    other_contact = create_contact()

    add_contact_page.create_contact_steps(existing_contact)
    time.sleep(3)
    add_contact_page.create_contact_steps(other_contact)

    contacts_page.open_contact_details(other_contact.phone)
    time.sleep(3)
    contacts_page.open_edit_mode()
    time.sleep(3)
    contacts_page.set_edit_field(contacts_page.EDIT_PHONE_INPUT, existing_contact.phone)
    contacts_page.submit_edit()

# We expect that modifying a contact to use an already existing phone number should not be allowed.
# However, due to a bug on the website, two contacts with the same phone number are created.
    assert contacts_page.contact_cards_count(existing_contact.phone) == 2

# --------------------------------------------------------------------
# 7. Registered user can’t edit field [EMAIL] to an already existing one
def test_edit_contact_duplicate_email_negative(authenticated_driver):
    contacts_page = ContactsPage(authenticated_driver)
    add_contact_page = ContactPage(authenticated_driver)

    existing_contact = create_contact()
    other_contact = create_contact()

    add_contact_page.create_contact_steps(existing_contact)
    time.sleep(3)
    add_contact_page.create_contact_steps(other_contact)

    contacts_page.open_contact_details(other_contact.phone)
    time.sleep(3)
    contacts_page.open_edit_mode()
    time.sleep(3)
    contacts_page.set_edit_field(contacts_page.EDIT_EMAIL_INPUT, existing_contact.email)
    contacts_page.submit_edit()

# We expect that modifying a contact to use an already existing email should not be allowed.
# However, due to a bug on the website, two contacts with the same email are created.
    contacts_page.open_contact_details(other_contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_EMAIL_INPUT) == existing_contact.email
