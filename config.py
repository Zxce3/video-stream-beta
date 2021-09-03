import os
from os import getenv

admins = {}
API_ID = int(os.getenv("API_ID", "6"))
API_HASH = os.getenv("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_NAME = os.getenv("SESSION_NAME")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "15"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
