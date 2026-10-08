from os import getenv
from dotenv import load_dotenv

load_dotenv()

BASE_URL = getenv("BASE_URL") #ivironment variable
EXITING_USER_EMAIL = getenv("EXITING_USER_EMAIL")
EXITING_USER_PASSWORD = getenv("EXITING_USER_PASSWORD")