# -*- coding: utf-8 -*-

token = '987654321:XXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
admin = '123456789'
ipc_host = '127.0.0.1'
ipc_port = 1242
ipc_password = ''

import logging
import re
import sys
import ASF_IPC as asf
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
pattern_2fa = re.compile(r'^\s*!?2[fF][aA]( +.+)?\s*$')

def mfa_timeout(bot, job):
    bot.editMessageText(chat_id=job.context[0], message_id=job.context[1], text='[2FA Deleted]')

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello!\nYou can send commands to your ASF bot.')

def reply(bot, update, job_queue):
    chat_id = update.message.chat_id
    command = update.message.text
    if isinstance(admin, str) and admin == str(chat_id) or isinstance(admin, list) and str(chat_id) in admin:
        try:
            res = api.command(command)
        except Exception as e:
            if hasattr(e, 'message'):
                res = e.message
            else:
                res = e.__class__.__name__
        if not isinstance(res, str):
            res = str(res)
        msg = update.message.reply_text(res, quote=True)
        if pattern_2fa.match(command):
            job_queue.run_once(mfa_timeout, 15, context=(chat_id, msg.message_id))
    else:
        update.message.reply_text('You don\'t have permission to use this bot!')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

api = asf.IPC(ipc_host, int(ipc_port), ipc_password)

updater = Updater(token)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, reply, pass_job_queue=True))
updater.dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()
