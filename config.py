import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
API_ID = int(os.getenv("API_ID", "6"))
API_HASH = os.getenv("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_NAME = os.getenv("SESSION_NAME")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "15"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "tg_video_stream")
BOT_USERNAME = getenv("BOT_USERNAME", "veezvidstreambot")
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! . ?").split())
