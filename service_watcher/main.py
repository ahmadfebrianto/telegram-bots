import os
from telethon import TelegramClient, events


def get_services_list():
    with open("services.txt") as f:
        # Parse comments and empty lines
        services = [
            line.strip()
            for line in f.readlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    return services


def is_service_running(service_name):
    status = os.system(f"systemctl is-active --quiet {service_name}")
    return status == 0


def main():

    # To get API_ID and API_HASH, visit https://my.telegram.org
    api_id = os.environ.get("TG_API_ID")
    api_hash = os.environ.get("TG_API_HASH")

    # To get BOT_TOKEN, visit https://t.me/BotFather
    bot_token = os.environ.get("TG_BOT_SVCWATCH")

    # To get USER_ID, visit https://t.me/userinfobot
    user_id = os.environ.get("TG_USER_ID")

    client = TelegramClient("svcwatcher", api_id, api_hash).start(bot_token=bot_token)

    @client.on(events.NewMessage(pattern="/status"))
    async def handler(event):

        # Check if the message is from the user.
        # If not, ignore it.
        if event.sender_id != int(user_id):
            return

        services = get_services_list()

        if not services:
            message = "No services to check."
            await event.respond(message)
            return

        message = "**Service Status**\n"

        for service in services:
            if is_service_running(service):
                message += f"\n- `{service}` ::: __running__. "
            else:
                message += f"\n- `{service}` ::: __not running__. "

        await event.respond(message)

    client.start()
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
