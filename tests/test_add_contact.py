from faker import Faker
from models.contact import Contact
from pages.add_contact_page import ContactPage
fake = Faker()

def test_add_contact_success_all_fields(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contact=Contact(
        fake.first_name(),
        fake.last_name(),
        fake.numerify("05##########"),
        fake.unique.email(),
        fake.city(),
        fake.text())

    add_contact_page.open_contact_form()
    add_contact_page.fill_contact(contact)
    add_contact_page.submit_contact()

    assert add_contact_page.contact_card_visible(contact.phone)

def test_add_contact_success_required_fields(authenticated_driver):
    add_contact_page = ContactPage(authenticated_driver)
    contact=Contact(
        fake.first_name(),
        fake.last_name(),
        fake.numerify("05##########"),
        fake.unique.email(),
        fake.city(),
        "")

    add_contact_page.open_contact_form()
    add_contact_page.fill_contact(contact)
    add_contact_page.submit_contact()

    assert add_contact_page.contact_card_visible(contact.phone)


