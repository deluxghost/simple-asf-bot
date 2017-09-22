# -*- coding: utf-8 -*-

token = '123456789:XXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXX'
admin = '987654321'
ipc = 'http://127.0.0.1:1242/IPC?command='

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
import urllib.parse as parse, urllib.request as request, urllib.error
import logging
import re
import sys

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
pattern_2fa = re.compile(r'^\s*!?2[fF][aA]( +.+)?\s*$')
pattern_sa = re.compile(r'^<(.+)>', re.M)
pattern_all = re.compile(r'@all\b')

def asf_ipc(command):
    command_all = pattern_all.search(command)
    if command_all:
        ret = list()
        for player in get_players():
            ret.append(asf_ipc(command.replace('@all', player)))
        return ''.join(ret).replace('\n\n', '\n')
    ipc_url = ipc + parse.quote(command)
    req = request.Request(ipc_url)
    try:
        res_data = request.urlopen(req)
    except urllib.error.HTTPError as e:
        return e.reason
    except urllib.error.URLError as e:
        return e.reason
    else:
        res = res_data.read().decode("utf-8")
        return res

def get_players():
    msg = asf_ipc('sa')
    players = pattern_sa.findall(msg)
    return players

def mfa_timeout(bot, job):
    bot.editMessageText(chat_id=job.context[0], message_id=job.context[1], text='[2FA Deleted]')

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello!\nYou can send commands to your ASF bot.')

def reply(bot, update, job_queue):
    chat_id = update.message.chat_id
    command = update.message.text
    if admin == str(chat_id):
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
