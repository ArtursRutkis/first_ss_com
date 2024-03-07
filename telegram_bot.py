import requests


def bot_send_message(text: str):
    TELEGRAM_TOKEN = "6953171077:AAH3j5jHyHFg_OUDC6wj2ZvRpW9e3n9nY1U"
    CHAT_ID = "-1002071459384"
    chat_message_text = (
        "https://api.telegram.org/bot"
        + TELEGRAM_TOKEN
        + "/sendMessage?chat_id="
        + CHAT_ID
        + "&text="
        + text
    )
    requests.get(chat_message_text)
