import telebot
import re
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8237808648:AAEY4bluOzClNSFOd79w4kjgTsL2rul-VZg"
OWNER = "dwaterlawh"   # without @

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"
ADMIN_FILE = "admins.json"

# ---------------- ADMIN SYSTEM ---------------- #

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

# ---------------- DATA SYSTEM ---------------- #

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

# ---------------- FIND NUMBER ---------------- #

def find_number(text,keywords):

    text = text.lower()

    for word in keywords:

        pattern = word + r"[\s\S]{0,20}?(\d+)"

        match = re.search(pattern,text)

        if match:
            return int(match.group(1))

    return 0

# ---------------- MAIN KEYBOARD ---------------- #

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

    kb.add(
        KeyboardButton("ADMIN PANEL")
    )

    return kb

# ---------------- ADMIN PANEL ---------------- #

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

# ---------------- START ---------------- #

@bot.message_handler(commands=['start'])
def start(message):

    if not is_admin(message):
        bot.send_message(message.chat.id,"Access denied")
        return

    bot.send_message(message.chat.id,"Select group",reply_markup=keyboard())

# ---------------- ADMIN PANEL OPEN ---------------- #

@bot.message_handler(func=lambda m: m.text == "ADMIN PANEL")
def open_admin(message):

    if message.from_user.username != OWNER:
        bot.send_message(message.chat.id,"Only owner can access admin panel")
        return

    bot.send_message(message.chat.id,"Admin Panel",reply_markup=admin_keyboard())

# ---------------- ADD ADMIN ---------------- #

@bot.message_handler(func=lambda m: m.text == "➕ Add Admin")
def add_admin(message):

    msg = bot.send_message(message.chat.id,"Send username like:\n@username")

    bot.register_next_step_handler(msg,process_add_admin)

def process_add_admin(message):

    username = message.text.replace("@","").lower()

    if username not in admins:

        admins.append(username)

        save_admins(admins)

        bot.send_message(message.chat.id,f"{username} added as admin")

    else:

        bot.send_message(message.chat.id,"Already admin")

# ---------------- REMOVE ADMIN ---------------- #

@bot.message_handler(func=lambda m: m.text == "➖ Remove Admin")
def remove_admin(message):

    msg = bot.send_message(message.chat.id,"Send username to remove")

    bot.register_next_step_handler(msg,process_remove_admin)

def process_remove_admin(message):

    username = message.text.replace("@","")

    if username in admins:

        admins.remove(username)

        save_admins(admins)

        bot.send_message(message.chat.id,f"{username} removed")

    else:

        bot.send_message(message.chat.id,"User not admin")

# ---------------- ADMIN LIST ---------------- #

@bot.message_handler(func=lambda m: m.text == "👥 Admin List")
def admin_list(message):

    bot.send_message(message.chat.id,"Admins:\n\n"+ "\n".join(admins))

# ---------------- BACK BUTTON ---------------- #

@bot.message_handler(func=lambda m: m.text == "🔙 Back")
def back_menu(message):

    bot.send_message(message.chat.id,"Main Menu",reply_markup=keyboard())

# ---------------- MAIN HANDLER ---------------- #

@bot.message_handler(content_types=['text','photo'])
def handle(message):

    global current_group

    if not is_admin(message):
        return

    text = (message.text if message.text else message.caption or "").lower()

# -------- GROUP SELECT -------- #

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

# -------- RESET -------- #

    if "reset" in text:

        for g in groups:
            groups[g] = {"reg":0,"ws":0,"active":0,"wd":0}

        save_data()

        bot.send_message(message.chat.id,"All totals reset")

        return

# -------- DAILY REPORT -------- #

    if "daily" in text:

        bot.send_message(message.chat.id,
        f"WIN03\n\nRegistrations: {groups['win03']['reg']}\nWS Task: {groups['win03']['ws']}\nActive Users: {groups['win03']['active']}\nWithdrawals: {groups['win03']['wd']}")

        bot.send_message(message.chat.id,
        f"SMART HUB\n\nRegistrations: {groups['smart']['reg']}\nWS Task: {groups['smart']['ws']}\nActive Users: {groups['smart']['active']}\nWithdrawals: {groups['smart']['wd']}")

        bot.send_message(message.chat.id,
        f"EARN TOGETHER\n\nRegistrations: {groups['earn']['reg']}\nWS Task: {groups['earn']['ws']}\nActive Users: {groups['earn']['active']}\nWithdrawals: {groups['earn']['wd']}")

        return

# -------- END REPORT -------- #

    if text.strip() == "end":

        g = groups[current_group]

        titles = {
            "win03":"WIN03",
            "smart":"SMART HUB",
            "earn":"EARN TOGETHER"
        }

        report = f"{titles[current_group]}\n\nRegistrations: {g['reg']}\nWS Task: {g['ws']}\nActive Users: {g['active']}\nWithdrawals: {g['wd']}"

        bot.send_message(message.chat.id,report)

        return

# -------- WORD FILTER -------- #

    reg = find_number(text,[
    "registration","registrations","register","registered",
    "today new subordinate","today new subordinates",
    "new subordinate","new subordinates",
    "new user","new users"
    ])

    ws = find_number(text,[
    "ws task","wa task","wa authorised","wa link",
    "whatsapp task","whatsapp authorised"
    ])

    active = find_number(text,[
    "active user","active users"
    ])

    wd = find_number(text,[
    "withdraw","withdrawal","withdrawals"
    ])

# -------- COUNTING -------- #

    if reg or ws or active or wd:

        groups[current_group]["reg"] += reg
        groups[current_group]["ws"] += ws
        groups[current_group]["active"] += active
        groups[current_group]["wd"] += wd

        save_data()

        g = groups[current_group]

        bot.send_message(
            message.chat.id,
            f"Counting...\n\nRegistrations: {g['reg']}\nWS Task: {g['ws']}\nActive Users: {g['active']}\nWithdrawals: {g['wd']}"
        )

bot.infinity_polling()
