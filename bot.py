import telebot
import re

TOKEN = "8237808648:AAEY4bluOzClNSFOd79w4kjgTsL2rul-VZg"

bot = telebot.TeleBot(TOKEN)

totals = {
    "reg":0,
    "ws":0,
    "active":0,
    "wd":0
}

def find_number(text, keyword):
    match = re.search(keyword + r".*?(\d+)", text.lower())
    if match:
        return int(match.group(1))
    return 0

@bot.message_handler(func=lambda message: True)
def count(message):

    text = message.text

    reg = find_number(text,"registration")
    ws = find_number(text,"task")
    active = find_number(text,"active")
    wd = find_number(text,"withdraw")

    totals["reg"] += reg
    totals["ws"] += ws
    totals["active"] += active
    totals["wd"] += wd

    bot.reply_to(message,
f"""TOTAL

Registrations: {totals['reg']}
WS Task: {totals['ws']}
Active Users: {totals['active']}
Withdrawals: {totals['wd']}
""")

bot.infinity_polling()
