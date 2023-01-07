# Service Watcher

A simple bot that watches for Systemd services status. If it detects a service is down, it will send a message.

## Setup

1. Install telethon

   ```bash
   pip install telethon
   ```

2. Create a new Telegram application and get the API ID and API hash. Save them in an environment variable called `TG_API_ID` and `TG_API_HASH` respectively. To do this, go to [my.telegram.org](https://my.telegram.org/auth) and create a new application.

3. Create a new Telegram bot and get the bot token. You can do this by following the instructions [here](https://core.telegram.org/bots#6-botfather). Save it in an environment variable called `TG_BOT_SVCWATCH`.

4. Get your Telegram user ID and save it in an environment variable called `TG_USER_ID`. You can do this by sending message to [userinfobot](https://t.me/userinfobot).

5. Add services to watch in services.txt. Each service should be on a new line.

6. Run the script

   ```bash
   python3 main.py
   ```
