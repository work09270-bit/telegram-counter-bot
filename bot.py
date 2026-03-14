import telebot
import re
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8237808648:AAEY4bluOzClNSFOd79w4kjgTsL2rul-VZg"

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"


def load_data():
    try:
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    except:
        return {
            "win03":{"reg":0,"ws":0,"active":0,"wd":0,"entries":0},
            "smart":{"reg":0,"ws":0,"active":0,"wd":0,"entries":0},
            "earn":{"reg":0,"ws":0,"active":0,"wd":0,"entries":0}
        }


def save_data():
    with open(DATA_FILE,"w") as f:
        json.dump(groups,f)


groups = load_data()
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
        KeyboardButton("📊 DAILY REPORT"),
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
        bot.send_message(message.chat.id,"📊 WIN03 selected\nSend WIN03 data\nType END when finished")
        return


    if "smart" in text:
        current_group = "smart"
        bot.send_message(message.chat.id,"💼 SMART HUB selected\nSend SMART HUB data\nType END when finished")
        return


    if "earn" in text:
        current_group = "earn"
        bot.send_message(message.chat.id,"💰 EARN TOGETHER selected\nSend EARN TOGETHER data\nType END when finished")
        return


    if "reset" in text:

        for g in groups:
            groups[g] = {"reg":0,"ws":0,"active":0,"wd":0,"entries":0}

        save_data()

        bot.send_message(message.chat.id,"🔄 All totals reset.")
        return


    if "daily" in text:

        bot.send_message(
            message.chat.id,
f"""📊 DAILY REPORT

📊 WIN03
Registrations: {groups['win03']['reg']}
WS Task: {groups['win03']['ws']}
Active Users: {groups['win03']['active']}
Withdrawals: {groups['win03']['wd']}

💼 SMART HUB EARNING
Registrations: {groups['smart']['reg']}
WS Task: {groups['smart']['ws']}
Active Users: {groups['smart']['active']}
Withdrawals: {groups['smart']['wd']}

💰 EARN TOGETHER
Registrations: {groups['earn']['reg']}
WS Task: {groups['earn']['ws']}
Active Users: {groups['earn']['active']}
Withdrawals: {groups['earn']['wd']}
"""
        )

      if "daily" in text:

    bot.send_message(
        message.chat.id,
f"""📊 WIN03

Registrations: {groups['win03']['reg']}
WS Task: {groups['win03']['ws']}
Active Users: {groups['win03']['active']}
Withdrawals: {groups['win03']['wd']}
"""
    )

    bot.send_message(
        message.chat.id,
f"""💼 SMART HUB EARNING

Registrations: {groups['smart']['reg']}
WS Task: {groups['smart']['ws']}
Active Users: {groups['smart']['active']}
Withdrawals: {groups['smart']['wd']}
"""
    )

    bot.send_message(
        message.chat.id,
f"""💰 EARN TOGETHER

Registrations: {groups['earn']['reg']}
WS Task: {groups['earn']['ws']}
Active Users: {groups['earn']['active']}
Withdrawals: {groups['earn']['wd']}
"""
    )

    bot.send_message(
        message.chat.id,
f"""Entries Counted

WIN03: {groups['win03']['entries']}
SMART HUB: {groups['smart']['entries']}
EARN TOGETHER: {groups['earn']['entries']}
"""
    )

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
        groups[current_group]["entries"] += 1

        save_data()


bot.infinity_polling()
