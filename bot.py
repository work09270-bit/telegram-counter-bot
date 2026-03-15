import telebot
import re
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8237808648:AAEY4bluOzClNSFOd79w4kjgTsL2rul-VZg"

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"


# -------------------------
# Load saved data
# -------------------------
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "win03": {"reg":0,"ws":0,"active":0,"wd":0},
            "smart": {"reg":0,"ws":0,"active":0,"wd":0},
            "earn": {"reg":0,"ws":0,"active":0,"wd":0}
        }


# -------------------------
# Save data
# -------------------------
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(groups, f)


groups = load_data()
current_group = None


# -------------------------
# STRONG NUMBER PARSER
# -------------------------
def find_number(text, keywords):

    text = text.lower()

    for word in keywords:

        pattern = word + r"[\s\S]{0,20}?(\d+)"

        match = re.search(pattern, text)

        if match:
            return int(match.group(1))

    return 0


# -------------------------
# Keyboard
# -------------------------
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


# -------------------------
# Start
# -------------------------
@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(
        message.chat.id,
        "Select a group:",
        reply_markup=keyboard()
    )


# -------------------------
# Main Handler
# -------------------------
@bot.message_handler(content_types=['text','photo'])
def handle(message):

    global current_group

    text = (message.text if message.text else message.caption or "").lower()


    # -------- GROUP SELECT --------

    if "win03" in text:

        current_group = "win03"

        bot.send_message(
            message.chat.id,
            "📊 WIN03 selected\nSend WIN03 data\nType END when finished"
        )
        return


    if "smart" in text:

        current_group = "smart"

        bot.send_message(
            message.chat.id,
            "💼 SMART HUB selected\nSend SMART HUB data\nType END when finished"
        )
        return


    if "earn" in text:

        current_group = "earn"

        bot.send_message(
            message.chat.id,
            "💰 EARN TOGETHER selected\nSend EARN data\nType END when finished"
        )
        return


    # -------- RESET --------

    if "reset" in text:

        for g in groups:
            groups[g] = {"reg":0,"ws":0,"active":0,"wd":0}

        save_data()

        bot.send_message(message.chat.id,"🔄 All totals reset")

        return


    # -------- DAILY REPORT --------

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

        return


    # -------- END REPORT --------

    if text.strip() == "end":

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


    # -------- NUMBER DETECTION --------

    reg = find_number(text,[
        "registration",
        "registrations",
        "register",
        "registered"
    ])

    ws = find_number(text,[
        "ws task",
        "wa task",
        "task authorised",
        "whatsapp task"
    ])

    active = find_number(text,[
        "active user",
        "active users",
        "active"
    ])

    wd = find_number(text,[
        "withdrawal",
        "withdrawals",
        "withdraw"
    ])


    if reg or ws or active or wd:

        groups[current_group]["reg"] += reg
        groups[current_group]["ws"] += ws
        groups[current_group]["active"] += active
        groups[current_group]["wd"] += wd

        save_data()


bot.infinity_polling()
