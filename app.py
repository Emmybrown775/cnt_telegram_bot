import re
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, URL
from wp import WP

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)



@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.effective_message.chat.id
    msg_id = update.effective_message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.effective_message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        bot_welcome = """
       Welcome to The CNT Open Heavens Bot, the bot is used to get daily open heavens from the CNT website.
       """
        # send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    elif text == "/make_post":
        wp = WP()
        result = wp.post_op()
        bot.sendMessage(chat_id=chat_id, text=result, reply_to_message_id=msg_id)
    elif text == "/get_date":
        wp = WP()
        result = wp.get_date()
        bot.sendMessage(chat_id=chat_id, text=result, reply_to_message_id=msg_id)
    elif text == "/get_last_post":
        wp = WP()
        result = wp.get_last_post()
        bot.sendMessage(chat_id=chat_id, text=result, reply_to_message_id=msg_id)
    else:
        wrong = "There is no such command"

        bot.sendMessage(chat_id=chat_id, text=wrong, reply_to_message_id=msg_id)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)
