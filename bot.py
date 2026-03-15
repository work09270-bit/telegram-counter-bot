import telebot
import re
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8237808648:AAEY4bluOzClNSFOd79w4kjgTsL2rul-VZg"

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"
ADMIN_FILE = "admins.json"

# -----------------------
# FIRST OWNER USERNAME
# -----------------------
OWNER = "dwaterlawh"   # ← change this to your telegram username


# -----------------------
# Load admins
# -----------------------
def load_admins():
    try:
        with open(ADMIN_FILE,"r") as f:
            return json.load(f)
    except:
        admins = [OWNER]
        save_admins(admins)
        return admins


def save_admins(admin_list):
    with open(ADMIN_FILE,"w") as f:
        json.dump(admin_list,f)


admins = load_admins()


# -----------------------
# Load data
# -----------------------
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


# -----------------------
# Admin check
# -----------------------
def is_admin(message):
    username = message.from_user.username
    return username in admins


# -----------------------
# Number finder
# -----------------------
def find_number(text, keywords):

    text = text.lower()

    for word in keywords:
        pattern = word + r"[\s\S]{0,20}?(\d+)"
        match = re.search(pattern,text)

        if match:
            return int(match.group(1))

    return 0


# -----------------------
# Main keyboard
# -----------------------
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


# -----------------------
# Admin keyboard
# -----------------------
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
        KeyboardButton("🔄 Reset Bot")
    )

    kb.add(
        KeyboardButton("🔙 Back")
    )

    return kb


# -----------------------
# Start
# -----------------------
@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(
        message.chat.id,
        "Select group",
        reply_markup=keyboard()
    )


# -----------------------
# Admin panel
# -----------------------
@bot.message_handler(commands=['admin'])
def admin_panel(message):

    if not is_admin(message):
        bot.send_message(message.chat.id,"Access denied")
        return

    bot.send_message(
        message.chat.id,
        "Admin Panel",
        reply_markup=admin_keyboard()
    )


# -----------------------
# Add admin
# -----------------------
@bot.message_handler(func=lambda m: m.text == "➕ Add Admin")
def add_admin(message):

    if not is_admin(message):
        return

    msg = bot.send_message(message.chat.id,"Send username\nExample:\n@username")

    bot.register_next_step_handler(msg,process_add_admin)


def process_add_admin(message):

    username = message.text.replace("@","")

    if username not in admins:

        admins.append(username)

        save_admins(admins)

        bot.send_message(message.chat.id,f"{username} added as admin")

    else:

        bot.send_message(message.chat.id,"Already admin")


# -----------------------
# Remove admin
# -----------------------
@bot.message_handler(func=lambda m: m.text == "➖ Remove Admin")
def remove_admin(message):

    if not is_admin(message):
        return

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


# -----------------------
# Admin list
# -----------------------
@bot.message_handler(func=lambda m: m.text == "👥 Admin List")
def admin_list(message):

    if not is_admin(message):
        return

    bot.send_message(message.chat.id,"Admins:\n\n"+ "\n".join(admins))


# -----------------------
# Reset bot
# -----------------------
@bot.message_handler(func=lambda m: m.text == "🔄 Reset Bot")
def reset_bot(message):

    if not is_admin(message):
        return

    for g in groups:
        groups[g] = {"reg":0,"ws":0,"active":0,"wd":0}

    save_data()

    bot.send_message(message.chat.id,"All totals reset")


# -----------------------
# Back
# -----------------------
@bot.message_handler(func=lambda m: m.text == "🔙 Back")
def back(message):

    bot.send_message(message.chat.id,"Main Menu",reply_markup=keyboard())


# -----------------------
# Main handler
# -----------------------
@bot.message_handler(content_types=['text','photo'])
def handle(message):

    global current_group

    text = (message.text if message.text else message.caption or "").lower()


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


    if "reset" in text:

        if not is_admin(message):
            bot.send_message(message.chat.id,"Only admins can reset")
            return

        for g in groups:
            groups[g] = {"reg":0,"ws":0,"active":0,"wd":0}

        save_data()

        bot.send_message(message.chat.id,"All totals reset")

        return


    if "daily" in text:

        bot.send_message(message.chat.id,
        "WIN03\n\nRegistrations: "+str(groups['win03']['reg'])+
        "\nWS Task: "+str(groups['win03']['ws'])+
        "\nActive Users: "+str(groups['win03']['active'])+
        "\nWithdrawals: "+str(groups['win03']['wd'])
        )

        bot.send_message(message.chat.id,
        "SMART HUB EARNING\n\nRegistrations: "+str(groups['smart']['reg'])+
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


    if text.strip() == "end":

        g = groups[current_group]

        titles = {
            "win03":"WIN03",
            "smart":"SMART HUB EARNING",
            "earn":"EARN TOGETHER"
        }

        report = titles[current_group]+"\n\nRegistrations: "+str(g['reg'])+"\nWS Task: "+str(g['ws'])+"\nActive Users: "+str(g['active'])+"\nWithdrawals: "+str(g['wd'])

        bot.send_message(message.chat.id,report)

        return


    reg = find_number(text,["registration","registrations","register","registered"])
    ws = find_number(text,["ws task","wa task","task authorised","whatsapp task"])
    active = find_number(text,["active user","active users","active"])
    wd = find_number(text,["withdrawal","withdrawals","withdraw"])


    if reg or ws or active or wd:
        groups[current_group]["reg"] += reg
        groups[current_group]["ws"] += ws
        groups[current_group]["active"] += active
        groups[current_group]["wd"] += wd

        save_data()


bot.infinity_polling()
