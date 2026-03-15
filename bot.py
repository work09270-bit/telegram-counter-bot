import telebot
import re
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8237808648:AAEY4bluOzClNSFOd79w4kjgTsL2rul-VZg"

OWNER = "dwaterlawh"   # change to your telegram username

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"
ADMIN_FILE = "admins.json"

# ----------------------
# LOAD ADMINS
# ----------------------

def load_admins():
    try:
        with open(ADMIN_FILE,"r") as f:
            return json.load(f)
    except:
        admins = [OWNER]
        save_admins(admins)
        return admins

def save_admins(admins):
    with open(ADMIN_FILE,"w") as f:
        json.dump(admins,f)

admins = load_admins()

# ----------------------
# LOAD DATA
# ----------------------

def load_data():
    try:
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    except:
        return {
            "win03":{"reg":0,"ws":0,"active":0,"wd":0},
            "smart":{"reg":0,"ws":0,"active":0,"wd":0},
            "earn":{"reg":0,"ws":0,"active":0,"wd":0}
        }

def save_data():
    with open(DATA_FILE,"w") as f:
        json.dump(groups,f)

groups = load_data()

current_group = None

# ----------------------
# ADMIN CHECK
# ----------------------

def is_admin(message):

    username = message.from_user.username

    if username in admins:
        return True

    return False

# ----------------------
# FIND NUMBER
# ----------------------

def find_number(text,keywords):

    text = text.lower()

    for word in keywords:

        pattern = word + r"[\s\S]{0,20}?(\d+)"

        match = re.search(pattern,text)

        if match:
            return int(match.group(1))

    return 0

# ----------------------
# KEYBOARD
# ----------------------

def keyboard():

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton("WIN03"),
        KeyboardButton("SMART HUB")
    )

    kb.add(
        KeyboardButton("EARN TOGETHER")
    )

    kb.add(
        KeyboardButton("DAILY REPORT"),
        KeyboardButton("RESET")
    )

    return kb

# ----------------------
# START
# ----------------------

@bot.message_handler(commands=['start'])
def start(message):

    if not is_admin(message):
        bot.send_message(message.chat.id,"Access denied")
        return

    bot.send_message(message.chat.id,"Select group",reply_markup=keyboard())

# ----------------------
# MAIN HANDLER
# ----------------------

@bot.message_handler(content_types=['text','photo'])
def handle(message):

    global current_group

    if not is_admin(message):
        return

    text = (message.text if message.text else message.caption or "").lower()

# ----------------------
# GROUP SELECT
# ----------------------

    if "win03" in text:

        current_group = "win03"

        bot.send_message(message.chat.id,"Send WIN03 data\nType END when finished")

        return

    if "smart" in text:

        current_group = "smart"

        bot.send_message(message.chat.id,"Send SMART HUB data\nType END when finished")

        return

    if "earn" in text:

        current_group = "earn"

        bot.send_message(message.chat.id,"Send EARN TOGETHER data\nType END when finished")

        return

# ----------------------
# RESET
# ----------------------

    if "reset" in text:

        for g in groups:
            groups[g] = {"reg":0,"ws":0,"active":0,"wd":0}

        save_data()

        bot.send_message(message.chat.id,"All totals reset")

        return

# ----------------------
# DAILY REPORT
# ----------------------

    if "daily" in text:

        bot.send_message(message.chat.id,
        "WIN03\n\nRegistrations: "+str(groups['win03']['reg'])+
        "\nWS Task: "+str(groups['win03']['ws'])+
        "\nActive Users: "+str(groups['win03']['active'])+
        "\nWithdrawals: "+str(groups['win03']['wd'])
        )

        bot.send_message(message.chat.id,
        "SMART HUB\n\nRegistrations: "+str(groups['smart']['reg'])+
        "\nWS Task: "+str(groups['smart']['ws'])+
        "\nActive Users: "+str(groups['smart']['active'])+
        "\nWithdrawals: "+str(groups['smart']['wd'])
        )
        bot.send_message(message.chat.id,
        "EARN TOGETHER\n\nRegistrations: "+str(groups['earn']['reg'])+
        "\nWS Task: "+str(groups['earn']['ws'])+
        "\nActive Users: "+str(groups['earn']['active'])+
        "\nWithdrawals: "+str(groups['earn']['wd'])
        )

        return

# ----------------------
# END REPORT
# ----------------------

    if text.strip() == "end":

        g = groups[current_group]

        titles = {
            "win03":"WIN03",
            "smart":"SMART HUB",
            "earn":"EARN TOGETHER"
        }

        report = titles[current_group]+"\n\nRegistrations: "+str(g['reg'])+"\nWS Task: "+str(g['ws'])+"\nActive Users: "+str(g['active'])+"\nWithdrawals: "+str(g['wd'])

        bot.send_message(message.chat.id,report)

        return

# ----------------------
# SMART WORD FILTER
# ----------------------

    reg = find_number(text,[
    "registration",
    "registrations",
    "register",
    "registered",
    "today new subordinate",
    "today new subordinates",
    "new subordinate",
    "new subordinates",
    "new user",
    "new users"
    ])

    ws = find_number(text,[
    "ws task",
    "wa task",
    "wa authorised",
    "wa link",
    "whatsapp task",
    "whatsapp authorised"
    ])

    active = find_number(text,[
    "active user",
    "active users"
    ])

    wd = find_number(text,[
    "withdraw",
    "withdrawal",
    "withdrawals"
    ])

# ----------------------
# ADD + SHOW LIVE COUNT
# ----------------------

    if reg or ws or active or wd:

        groups[current_group]["reg"] += reg
        groups[current_group]["ws"] += ws
        groups[current_group]["active"] += active
        groups[current_group]["wd"] += wd

        save_data()

        g = groups[current_group]

        bot.send_message(
            message.chat.id,
            "Counting...\n\n"
            "Registrations: "+str(g["reg"])+
            "\nWS Task: "+str(g["ws"])+
            "\nActive Users: "+str(g["active"])+
            "\nWithdrawals: "+str(g["wd"])
        )

bot.infinity_polling()
