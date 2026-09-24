from faker import Faker
from models.user import User
fake = Faker()

def create_user(email = None, password = None):
    return User(
        email = email if email is not None else fake.unique.email(),
        password = password if password is not None else fake.password(
            length=12, special_chars=True,digits=True, upper_case=True,lower_case=True
        )
    )

EXITING_USER_EMAIL = "anna12345@gmail.com"
EXITING_USER_PASSWORD = "123456!Anna"

INVALID_EMAIL = "anna12345gmail.com"
INVALID_PASSWORD = "000"

def exiting_user():
    return create_user(email = EXITING_USER_EMAIL, password = EXITING_USER_PASSWORD)

def invalid_email_user():
    return create_user(email = INVALID_EMAIL, password = EXITING_USER_PASSWORD)

def invalid_password_user():
    return create_user(email = EXITING_USER_EMAIL, password = INVALID_PASSWORD)