import json

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

BOT_TOKEN = config["BOT_TOKEN"]
ADMIN_ID = config["ADMIN_ID"]
GREETING_TEXT = config["GREETING_TEXT"]
GREETING_IMAGE_URL = config["GREETING_IMAGE_URL"]