import requests
from config import config

def webhook(message):
    message=f'<@{config["discordUserId"]}> '+message
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    url = config['discordHook']
    info = '{"content" : "' + message + '"}'
    data = info.encode()
    requests.post(url, headers=headers, data=data)

# webhook("webhook test..")