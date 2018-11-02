import asyncio
import configparser
import logging
import sys

from aiotg import Bot, Chat
from ASF import IPC

if len(sys.argv) < 2:
    print('usage: python simple.py simple.conf')
    sys.exit(1)
conf = sys.argv[1]
config = configparser.ConfigParser()
config.read(conf)
BOT_TOKEN = config.get('telegram', 'bot_token', fallback='')
ADMIN_ID = int(config.get('telegram', 'admin_id', fallback=0))
ADDRESS = config.get('ipc', 'address', fallback='http://127.0.0.1:1242/')
PASSWORD = config.get('ipc', 'password', fallback='')

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('simple_asf_bot')

bot = Bot(BOT_TOKEN)


async def command(asf, cmd):
    return await asf.Api.Command['command'].post(command=cmd)


async def main():
    async with IPC(ipc=ADDRESS, password=PASSWORD) as asf:
        @bot.command(r'^([^/].*)$')
        async def message(chat: Chat, match):
            sender = chat.sender['id']
            logger.info(f'Get {match.group(1)}')
            if sender == ADMIN_ID:
                resp = await command(asf, match.group(1))
                reply = resp.result if resp.success else resp.message
            else:
                reply = 'You have no permission to use this bot!'
            logger.info(f'Ret {reply}')
            await chat.send_text(reply)
        await bot.loop()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
