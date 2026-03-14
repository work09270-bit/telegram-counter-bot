import telebot
import re

TOKEN = "8237808648:AAEY4bluOzClNSFOd79w4kjgTsL2rul-VZg"

bot = telebot.TeleBot(TOKEN)

groups = {
    "win03": {"reg":0,"ws":0,"active":0,"wd":0},
    "smart": {"reg":0,"ws":0,"active":0,"wd":0},
    "earn": {"reg":0,"ws":0,"active":0,"wd":0}
}

current_group = "win03"

def find(text, word):
    match = re.search(word + r".*?(\d+)", text.lower())
    if match:
        return int(match.group(1))
    return 0

@bot.message_handler(func=lambda m: True)
def handle(message):

    global current_group
    text = message.text.lower()

    # switch group
    if "win03" in text:
        current_group = "win03"
        bot.reply_to(message,"WIN03 selected")
        return

    if "smart" in text:
        current_group = "smart"
        bot.reply_to(message,"SMART HUB selected")
        return

    if "earn" in text:
        current_group = "earn"
        bot.reply_to(message,"EARN TOGETHER selected")
        return

    # reset
    if "reset" in text:
        for g in groups:
            groups[g] = {"reg":0,"ws":0,"active":0,"wd":0}
        bot.reply_to(message,"All totals reset")
        return

    # end command
    if "end" in text:
        g = groups[current_group]
        bot.reply_to(message,
f"""{current_group.upper()} REPORT

Registrations: {g['reg']}
WS Task Authorised: {g['ws']}
Active Users: {g['active']}
Withdrawals: {g['wd']}
""")
        return

    # extract numbers
    reg = find(text,"registration")
    ws = find(text,"task")
    active = find(text,"active")
    wd = find(text,"withdraw")

    groups[current_group]["reg"] += reg
    groups[current_group]["ws"] += ws
    groups[current_group]["active"] += active
    groups[current_group]["wd"] += wd

    g = groups[current_group]

    bot.reply_to(message,
f"""UPDATED TOTAL

Registrations: {g['reg']}
WS Task Authorised: {g['ws']}
Active Users: {g['active']}
Withdrawals: {g['wd']}
""")

bot.infinity_polling()
