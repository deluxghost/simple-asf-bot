# -*- coding: utf-8 -*-

token = '123456789:XXXXXX-XXXXXXXXXXXXXXXXXXXXX'
admin = '987654321'
ipc_password = ''
ipc = 'http://127.0.0.1:1242/Api/Command/'

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
import urllib.parse as parse, urllib.request as request, urllib.error
import json
import logging
import re
import sys

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
pattern_2fa = re.compile(r'^\s*!?2[fF][aA]( +.+)?\s*$')

def asf_ipc(command):
    ipc_url = ipc + parse.quote(command)
    req = request.Request(ipc_url)
    if ipc_password:
        req.add_header("Authentication", ipc_password)
    try:
        data = ''.encode('utf-8')
        resp = request.urlopen(req, data=data)
    except urllib.error.HTTPError as e:
        return '{0} - {1}'.format(str(e.code), e.reason)
    except urllib.error.URLError as e:
        return e.reason
    else:
        res = resp.read().decode("utf-8")
        return json_parse(res)

def json_parse(incoming):
    data = json.loads(incoming)
    if data.get('Success'):
        result = data.get('Result')
        return result
    return data.get('Message')

def mfa_timeout(bot, job):
    bot.editMessageText(chat_id=job.context[0], message_id=job.context[1], text='[2FA Deleted]')

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello!\nYou can send commands to your ASF bot.')

def reply(bot, update, job_queue):
    chat_id = update.message.chat_id
    command = update.message.text
    if isinstance(admin, str) and admin == str(chat_id) or isinstance(admin, list) and str(chat_id) in admin:
        res = asf_ipc(command)
        if not isinstance(res, str):
            res = str(res)
        msg = update.message.reply_text(res, quote=True)
        if pattern_2fa.match(command):
            job_queue.run_once(mfa_timeout, 15, context=(chat_id, msg.message_id))
    else:
        update.message.reply_text('You don\'t have permission to use this bot!', quote=True)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, reply, pass_job_queue=True))
updater.dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()
