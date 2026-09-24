from faker import Faker
from models.contact import Contact
fake = Faker

def create_contact(name = None, last_name = None, phone = None, email = None, address = None, description = None):
    return Contact(
        name = name if name is not None else fake.first_name(),
        last_name = last_name if last_name is not None else fake.last_name(),
        phone = phone if phone is not None else fake.numerify("050#########"),
        email = email if email is not None else fake.unique.email(),
        address = address if address is not None else fake.city(),
        description = description if description is not None else fake.sentence(nb_words=5))


