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


def find(text, words):
    for w in words:
        match = re.search(w + r".*?(\d+)", text.lower())
        if match:
            return int(match.group(1))
    return 0


def keyboard():

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton("📊 WIN03"),
        KeyboardButton("💼 SMART HUB EARNING")
    )

    kb.add(
        KeyboardButton("💰 EARN TOGETHER")
    )

    kb.add(
        KeyboardButton("🔄 RESET")
    )

    return kb


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(
        message.chat.id,
        "Select a group:",
        reply_markup=keyboard()
    )


@bot.message_handler(func=lambda m: True)
def handle(message):

    global current_group
    text = message.text.lower()

    if "win03" in text:
        current_group = "win03"
        return

    if "smart" in text:
        current_group = "smart"
        return

    if "earn" in text:
        current_group = "earn"
        return


    if "reset" in text:

        for g in groups:
            groups[g] = {"reg":0,"ws":0,"active":0,"wd":0}

        bot.send_message(message.chat.id,"🔄 All totals reset.")
        return


    if text == "end":

        g = groups[current_group]

        titles = {
            "win03":"📊 WIN03",
            "smart":"💼 SMART HUB EARNING",
            "earn":"💰 EARN TOGETHER"
        }

        bot.send_message(
            message.chat.id,
f"""{titles[current_group]}

Registrations: {g['reg']}
WS Task: {g['ws']}
Active Users: {g['active']}
Withdrawals: {g['wd']}
"""
        )

        return


    reg = find(text,["registration","register"])
    ws = find(text,["task","authorised","wa"])
    active = find(text,["active"])
    wd = find(text,["withdraw"])

    if reg or ws or active or wd:

        groups[current_group]["reg"] += reg
        groups[current_group]["ws"] += ws
        groups[current_group]["active"] += active
        groups[current_group]["wd"] += wd


bot.infinity_polling()
