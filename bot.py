# -*- coding: utf-8 -*-

token = '123456789:XXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXX'
admin = '987654321'
ipc = 'http://127.0.0.1:1242/IPC?command='

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.parse as parse, urllib.request as request
import logging
import sys

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def asf_ipc(command):
    ipc_url = ipc + parse.quote(command)
    req = request.Request(ipc_url)
    res_data = request.urlopen(req)
    res = res_data.read().decode("utf-8")
    return res

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello!\nYou can send commands to your ASF bot.')

def reply(bot, update):
    if admin == str(update.message.chat_id):
        bot.sendMessage(update.message.chat_id, text=asf_ipc(update.message.text))
    else:
        bot.sendMessage(update.message.chat_id, text='You don\'t have permission to use this bot!')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, reply))
updater.dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()
