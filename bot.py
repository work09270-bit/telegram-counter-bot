import telebot
import re
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8237808648:AAEY4bluOzClNSFOd79w4kjgTsL2rul-VZg"

bot = telebot.TeleBot(TOKEN)

groups = {
    "win03": {"reg":0,"ws":0,"active":0,"wd":0},
    "smart": {"reg":0,"ws":0,"active":0,"wd":0},
    "earn": {"reg":0,"ws":0,"active":0,"wd":0}
}

current_group = None


def find(text, word):
    match = re.search(word + r".*?(\d+)", text.lower())
    if match:
        return int(match.group(1))
    return 0


# start command
@bot.message_handler(commands=['start'])
def start(message):

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(
        KeyboardButton("WIN03"),
        KeyboardButton("SMART HUB EARNING"),
        KeyboardButton("EARN TOGETHER")
    )

    bot.send_message(
        message.chat.id,
        "Select a group:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda m: True)
def handle(message):

    global current_group
    text = message.text.lower()

    if "win03" in text:
        current_group = "win03"
        bot.reply_to(message,"Start sending WIN03 data.\nSend END when finished.")
        return

    if "smart" in text:
        current_group = "smart"
        bot.reply_to(message,"Start sending SMART HUB data.\nSend END when finished.")
        return

    if "earn" in text:
        current_group = "earn"
        bot.reply_to(message,"Start sending EARN TOGETHER data.\nSend END when finished.")
        return

    if text == "end":

        g = groups[current_group]

        title = {
            "win03":"WIN03",
            "smart":"SMART HUB EARNING",
            "earn":"EARN TOGETHER"
        }

        bot.send_message(
            message.chat.id,
f"""{title[current_group]}

Registrations: {g['reg']}
WS Task: {g['ws']}
Active Users: {g['active']}
Withdrawals: {g['wd']}
"""
        )

        return

    reg = find(text,"registration")
    ws = find(text,"task")
    active = find(text,"active")
    wd = find(text,"withdraw")

    groups[current_group]["reg"] += reg
    groups[current_group]["ws"] += ws
    groups[current_group]["active"] += active
    groups[current_group]["wd"] += wd


bot.infinity_polling()
