import telebot
import re
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8237808648:AAEY4bluOzClNSFOd79w4kjgTsL2rul-VZg"
OWNER_ID = 8137930541  # your telegram numeric ID

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"
ADMIN_FILE = "admins.json"

# ---------------- ADMIN SYSTEM ---------------- #

def load_admins():
    try:
        with open(ADMIN_FILE,"r") as f:
            return json.load(f)
    except:
        admins = [OWNER_ID]
        save_admins(admins)
        return admins

def save_admins(admins):
    with open(ADMIN_FILE,"w") as f:
        json.dump(admins,f)

admins = load_admins()

def is_admin(user_id):
    return user_id in admins


# ---------------- DATA SYSTEM ---------------- #

def empty_group():
    return {"reg":[],"ws":[],"active":[],"wd":[]}

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

# store selected group per chat
chat_group = {}

# ---------------- FIND NUMBER ---------------- #

def find_number(text,keywords):

    for word in keywords:

        pattern = rf"{word}[^0-9]*(\d+)"

        match = re.search(pattern,text)

        if match:
            return int(match.group(1))

    return 0


# ---------------- FORMAT CALC ---------------- #

def calc(numbers):

    if not numbers:
        return "0"

    total = sum(numbers)

    if len(numbers) == 1:
        return str(total)

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

    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id,"Access denied")
        return

    bot.send_message(message.chat.id,"Select group",reply_markup=keyboard())


# ---------------- MAIN HANDLER ---------------- #

@bot.message_handler(content_types=['text','photo'])
def handle(message):

    if not is_admin(message.from_user.id):
        return

    chat_id = message.chat.id

    text = (message.text if message.text else message.caption or "").lower()


# -------- GROUP SELECT -------- #

    if text == "win03":

        chat_group[chat_id] = "win03"

        bot.send_message(chat_id,"Send WIN03 data\nType END when finished")
        return


    if text == "smart hub":

        chat_group[chat_id] = "smart"

        bot.send_message(chat_id,"Send SMART HUB data\nType END when finished")
        return


    if text == "earn together":

        chat_group[chat_id] = "earn"

        bot.send_message(chat_id,"Send EARN TOGETHER data\nType END when finished")
        return


# -------- RESET -------- #

    if text == "reset":

        for g in groups:
            groups[g] = empty_group()

        save_data()

        bot.send_message(chat_id,"All totals reset")
        return


# -------- DAILY REPORT -------- #

    if text == "daily report":

        titles = {
            "win03":"WIN03",
            "smart":"SMART HUB",
            "earn":"EARN TOGETHER"
        }

        for g in groups:

            data = groups[g]

            msg = f"""
{titles[g]}

Registrations
{calc(data['reg'])}

WS Task
{calc(data['ws'])}

Active Users
{calc(data['active'])}

Withdrawals
{calc(data['wd'])}
"""

            bot.send_message(chat_id,msg)

        return


# -------- END REPORT -------- #

    if text == "end":

        if chat_id not in chat_group:
            bot.send_message(chat_id,"Select group first")
            return

        gname = chat_group[chat_id]

        g = groups[gname]

        titles = {
            "win03":"WIN03",
            "smart":"SMART HUB",
            "earn":"EARN TOGETHER"
        }

        report = f"""
{titles[gname]}

Registrations
{calc(g['reg'])}

WS Task
{calc(g['ws'])}

Active Users
{calc(g['active'])}

Withdrawals
{calc(g['wd'])}
"""

        bot.send_message(chat_id,report)

        return


# -------- REQUIRE GROUP -------- #

    if chat_id not in chat_group:
        return

    group = chat_group[chat_id]


# -------- DETECT NUMBERS -------- #

    reg = find_number(text,[
    "registration","register","new subordinate","new user"
    ])

    ws = find_number(text,[
    "ws task","wa task","wa link","whatsapp task"
    ])

    active = find_number(text,[
    "active user","active users"
    ])

    wd = find_number(text,[
    "withdraw","withdrawal"
    ])


# -------- COUNT -------- #

    if reg:
        groups[group]["reg"].append(reg)

    if ws:
        groups[group]["ws"].append(ws)

    if active:
        groups[group]["active"].append(active)

    if wd:
        groups[group]["wd"].append(wd)

    if reg or ws or active or wd:

        save_data()

        g = groups[group]

        bot.send_message(
            chat_id,
            f"""
Counting...

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
