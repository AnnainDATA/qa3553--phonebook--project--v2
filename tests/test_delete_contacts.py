#pytest -v tests/test_delete_contacts.py
import logging
import pytest
from data.contact_data import create_contact
from pages.add_contact_page import ContactPage
from pages.contacts_page import ContactsPage

logger = logging.getLogger(__name__)

@pytest.mark.skip(reason="not relevant")
def test_delete_contacts_by_one(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

# create new contact
    contact = create_contact()
    add_contact_page.create_contact_steps(contact)
# contact cards count
    contact_count_before = contacts_page.all_contact_cards_count()
# delete new contact
    contacts_page.open_contact_details(contact.phone)
    contacts_page.remove_contact()
# contact cards count
    contact_count_now = contacts_page.all_contact_cards_count()

    assert contact_count_now == contact_count_before-1


def test_delete_contact_decreases_list_by_one(ensure_min_contacts):
    logger.info("Test: test_delete_contact_decreases_list_by_one")
    contacts_page = ContactsPage(ensure_min_contacts)

    contacts_page.open_contact_list()
    count_before = contacts_page.total_contacts_count()
    logger.info(f"Contacts before: {count_before}")

    contacts_page.open_first_contact()
    contacts_page.remove_contact()
    count_after = contacts_page.total_contacts_count()
    logger.info(f"Contacts after: {count_after}")

    assert count_after == count_before-1


def test_delete_all_contacts(ensure_min_contacts):
    contacts_page = ContactsPage(ensure_min_contacts)

    contacts_page.open_contact_list()
    contacts_page.delete_all_contacts()
    assert contacts_page.total_contacts_count() == 0

