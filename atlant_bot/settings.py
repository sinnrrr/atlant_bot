import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BOT_TOKEN = os.environ["BOT_TOKEN"]
DB_URI = os.environ["DB_URI"]
DB_NAME = os.environ["DB_NAME"]
GAZOVIK_USERNAME = os.environ["GAZOVIK_USERNAME"]
GAZOVIK_PASSWORD = os.environ["GAZOVIK_PASSWORD"]
STORAGE_FILENAME = os.environ["STORAGE_FILENAME"]
LOGIN_URL = "https://energyplus.ng-club.com/ua/auth/login"
