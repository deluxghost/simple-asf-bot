# Simple ASF Bot

Send commands to ASF in Telegram.

## Requirements

* Python 3.6+
* aiotg
* ASF_IPC

## Installation

```shell
git clone https://github.com/deluxghost/simple-asf-bot
cd simple-asf-bot
pip3 install -r requirements.txt
```

## Configuration

Edit `simple.conf`:

```ini
[telegram]
bot_token = 987654321:XXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXX  ; The API token of your Telegram bot
admin_id = 123456789  ; Your Telegram number ID (not the username)
proxy = socks5://127.0.0.1:1234  ; Proxy URL for Telegram request, empty if you don't use proxy

[ipc]
address = http://127.0.0.1:1242/  ; ASF IPC address
password = PASSWORD  ; ASF IPC password
```

## Getting Started

```shell
python3 simple.py simple.conf
```
