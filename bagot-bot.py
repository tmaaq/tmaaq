import telebot
import os
from flask import Flask, request
import logging

bot = telebot.TeleBot('1119016973:AAGKeP-J6VDcr3LpEa8WYNu63yA_eh0zBIU');

@bot.message_handler(commands=['start'])
def handle_text(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True,False)
    user_markup.row('/start','/info')
    start_text = str('Привет, '+message.from_user.first_name+'!\nЯ бот на Heroku.')
    bot.send_message(chat_id=1154965888, text=start_text, parse_mode='Markdown')

if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://test-new-new.herokuapp.com") 
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 60))
else:
    bot.remove_webhook()
    bot.polling(none_stop=True)
