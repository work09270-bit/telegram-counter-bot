import telebot
import re
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8237808648:AAEY4bluOzClNSFOd79w4kjgTsL2rul-VZg"
OWNER = "dwaterlawh"

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"
ADMIN_FILE = "admins.json"

# ---------- ADMIN SYSTEM ---------- #

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

def is_admin(message):
    username = message.from_user.username
    return username in admins


# ---------- DATA SYSTEM ---------- #

def empty_group():
    return {
        "reg":[],
        "ws":[],
        "active":[],
        "wd":[],
        "entries":0
    }

def load_data():
    try:
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    except:
        return {
            "win03":empty_group(),
            "smart":empty_group(),
            "earn":empty_group()
        }

groups = load_data()

def save_data():
    with open(DATA_FILE,"w") as f:
        json.dump(groups,f)

current_group = None


# ---------- NUMBER FIND ---------- #

def find_number(text,keywords):

    for word in keywords:

        pattern = word + r"[\s\S]{0,20}?(\d+)"

        match = re.search(pattern,text)

        if match:
            return int(match.group(1))

    return 0


# ---------- KEYBOARD ---------- #

def keyboard():

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton("📊 WIN03"),
        KeyboardButton("📊 SMART HUB")
    )

    kb.add(
        KeyboardButton("📊 EARN TOGETHER")
    )

    kb.add(
        KeyboardButton("📑 DAILY REPORT"),
        KeyboardButton("♻ RESET")
    )

    kb.add(
        KeyboardButton("⚙ ADMIN PANEL")
    )

    return kb


def admin_keyboard():

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton("➕ Add Admin"),
        KeyboardButton("➖ Remove Admin")
    )

    kb.add(
        KeyboardButton("👥 Admin List")
    )

    kb.add(
        KeyboardButton("🔙 Back")
    )

    return kb


# ---------- START ---------- #

@bot.message_handler(commands=['start'])
def start(message):

    if not is_admin(message):
        bot.send_message(message.chat.id,"Access denied")
        return

    bot.send_message(message.chat.id,"📌 Select group",reply_markup=keyboard())


# ---------- ADMIN PANEL ---------- #

@bot.message_handler(func=lambda m: m.text == "⚙ ADMIN PANEL")
def open_admin(message):

    if message.from_user.username != OWNER:
        bot.send_message(message.chat.id,"Only owner can access admin panel")
        return

    bot.send_message(message.chat.id,"Admin Panel",reply_markup=admin_keyboard())


# ---------- ADD ADMIN ---------- #

@bot.message_handler(func=lambda m: m.text == "➕ Add Admin")
def add_admin(message):

    msg = bot.send_message(message.chat.id,"Send username like\n@username")

    bot.register_next_step_handler(msg,process_add_admin)


def process_add_admin(message):

    username = message.text.replace("@","")

    if username not in admins:

        admins.append(username)

        save_admins(admins)

        bot.send_message(message.chat.id,f"@{username} added as admin")

        bot.send_message(message.chat.id,f"🎉 @{username} has been promoted to admin")

    else:

        bot.send_message(message.chat.id,"Already admin")


# ---------- REMOVE ADMIN ---------- #

@bot.message_handler(func=lambda m: m.text == "➖ Remove Admin")
def remove_admin(message):

    msg = bot.send_message(message.chat.id,"Send username")

    bot.register_next_step_handler(msg,process_remove_admin)


def process_remove_admin(message):

    username = message.text.replace("@","")

    if username in admins:

        admins.remove(username)

        save_admins(admins)

        bot.send_message(message.chat.id,f"{username} removed")

    else:

        bot.send_message(message.chat.id,"User not admin")


# ---------- ADMIN LIST ---------- #

@bot.message_handler(func=lambda m: m.text == "👥 Admin List")
def admin_list(message):

    bot.send_message(message.chat.id,"\n".join(["@"+a for a in admins]))


# ---------- BACK ---------- #

@bot.message_handler(func=lambda m: m.text == "🔙 Back")
def back(message):

    bot.send_message(message.chat.id,"Main Menu",reply_markup=keyboard())


# ---------- MAIN HANDLER ---------- #

@bot.message_handler(content_types=['text','photo'])
def handle(message):

    global current_group

    if not is_admin(message):
        return

    text = (message.text if message.text else message.caption or "").lower()

# ---- GROUP SELECT ---- #

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


# ---- RESET ---- #

    if "reset" in text:

        for g in groups:
            groups[g] = empty_group()

        save_data()

        bot.send_message(message.chat.id,"All totals reset")
        return


# ---- END ---- #

    if text.strip() == "end":

        g = groups[current_group]

        titles = {
            "win03":"WIN03",
            "smart":"SMART HUB",
            "earn":"EARN TOGETHER"
        }

        # calculation message

        calc_msg = f"""{titles[current_group]} COUNTED DATA

Registrations
{' + '.join(map(str,g['reg']))}

WS Task
{' + '.join(map(str,g['ws']))}

Active Users
{' + '.join(map(str,g['active']))}

Withdrawals
{' + '.join(map(str,g['wd']))}

Total Entries Counted: {g['entries']}
"""

        bot.send_message(message.chat.id,calc_msg)

        # final report

        final_msg = f"""{titles[current_group]}

Registrations: {sum(g['reg'])}
WS Task: {sum(g['ws'])}
Active Users: {sum(g['active'])}
Withdrawals: {sum(g['wd'])}
"""

        bot.send_message(message.chat.id,final_msg)

        return


# ---- COUNT ---- #

    reg = find_number(text,["registration","new subordinate","new user"])
    ws = find_number(text,["ws task","wa task","whatsapp"])
    active = find_number(text,["active user"])
    wd = find_number(text,["withdraw"])

    if reg or ws or active or wd:

        if reg:
            groups[current_group]["reg"].append(reg)

        if ws:
            groups[current_group]["ws"].append(ws)

        if active:
            groups[current_group]["active"].append(active)

        if wd:
            groups[current_group]["wd"].append(wd)

        groups[current_group]["entries"] += 1

        save_data()

        bot.send_message(message.chat.id,"Counting...")

bot.infinity_polling()
