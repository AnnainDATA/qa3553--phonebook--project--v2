import pytest
from faker import Faker
fake = Faker()

PHONE_ALERT_TEXT = "Phone not valid: Phone number must contain only digits! And length min 10, max 15!"
EMAIL_ALERT_TEXT = "Email not valid: must be a well-formed email address"

# INVALID_CONTACT_FIELDS = [
#     pytest.param("phone", "0504", PHONE_ALERT_TEXT, id="phone_too_short"),
#     pytest.param("phone", fake.numerify("#" * 20), PHONE_ALERT_TEXT, id="phone_too_long"),
#     pytest.param("phone", "jfhkdfghkfdh", PHONE_ALERT_TEXT, id="phone_leters"),
#     pytest.param("email", "dkjvkfdfkjkfdj", EMAIL_ALERT_TEXT, id="email_letters"),
#     pytest.param("email", "invalid_email_format", EMAIL_ALERT_TEXT, id="invalid_email_format"),
#     pytest.param("email", "@חיחךח", EMAIL_ALERT_TEXT, id="hebrew"),
#     pytest.param("email", "f@.kldf", EMAIL_ALERT_TEXT, id="dot_after_at"),
#
# ]
#
# SUCCESS_DESCRIPTIONS = [
#     pytest.param(None, id="all_fields"),
#     pytest.param("", id="required_fields_only")
# ]


