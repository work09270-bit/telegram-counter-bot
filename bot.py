import telebot
import re
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8237808648:AAEY4bluOzClNSFOd79w4kjgTsL2rul-VZg"
OWNER = "dwaterlawh"

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

def empty_group():
    return {
        "reg":[],
        "ws":[],
        "active":[],
        "wd":[]
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

# ---------------- FORMAT CALCULATION ---------------- #

def calc(numbers):

    if not numbers:
        return "0"

    total = sum(numbers)

    if len(numbers) == 1:
        return f"{numbers[0]} = {total}"

    return " + ".join(map(str,numbers)) + f" = {total}"

# ---------------- KEYBOARD ---------------- #

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

# ---------------- START ---------------- #

@bot.message_handler(commands=['start'])
def start(message):

    if not is_admin(message):
        bot.send_message(message.chat.id,"Access denied")
        return

    bot.send_message(message.chat.id,"Select group",reply_markup=keyboard())

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
            groups[g] = empty_group()

        save_data()

        bot.send_message(message.chat.id,"All totals reset")
        return

# -------- DAILY REPORT -------- #

    if "daily" in text:

        titles = {
            "win03":"WIN03",
            "smart":"SMART HUB",
            "earn":"EARN TOGETHER"
        }

        for g in groups:

            data = groups[g]

            msg = f"""{titles[g]}

Registrations
{calc(data['reg'])}

WS Task
{calc(data['ws'])}

Active Users
{calc(data['active'])}

Withdrawals
{calc(data['wd'])}
"""

            bot.send_message(message.chat.id,msg)

        return

# -------- END REPORT -------- #

    if text.strip() == "end":

        g = groups[current_group]

        titles = {
            "win03":"WIN03",
            "smart":"SMART HUB",
            "earn":"EARN TOGETHER"
        }

        report = f"""{titles[current_group]}

Registrations
{calc(g['reg'])}

WS Task
{calc(g['ws'])}

Active Users
{calc(g['active'])}

Withdrawals
{calc(g['wd'])}
"""

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

        if reg:
            groups[current_group]["reg"].append(reg)

        if ws:
            groups[current_group]["ws"].append(ws)

        if active:
            groups[current_group]["active"].append(active)

        if wd:
            groups[current_group]["wd"].append(wd)

        save_data()

        g = groups[current_group]

        bot.send_message(
            message.chat.id,
            f"""Counting...

Registrations
{calc(g['reg'])}

WS Task
{calc(g['ws'])}

Active Users
{calc(g['active'])}

Withdrawals
{calc(g['wd'])}
"""
        )

bot.infinity_polling()
