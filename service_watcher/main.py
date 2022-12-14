import os
from asyncio import sleep

from telethon import TelegramClient, events


class ServiceWatcher:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_services_list():
        with open("services.txt") as f:
            # Parse comments and empty lines
            services = [
                line.strip()
                for line in f.readlines()
                if line.strip() and not line.strip().startswith("#")
            ]
        return services

    @staticmethod
    def is_service_running(service_name):
        status = os.system(f"systemctl is-active --quiet {service_name}")
        return status == 0

    def get_services_status(self):
        services = self.get_services_list()
        if not services:
            return "No services to check."

        message = "**Service Status**\n"

        for service in services:
            if self.is_service_running(service):
                message += f"\n- `{service}` ::: __running__. "
            else:
                message += f"\n- `{service}` ::: __not running__. "

        return message


def main():
    api_id = os.environ.get("TG_API_ID")
    api_hash = os.environ.get("TG_API_HASH")
    bot_token = os.environ.get("TG_BOT_SVCWATCH")
    user_id = os.environ.get("TG_USER_ID")

    client = TelegramClient("svcwatcher", api_id, api_hash).start(bot_token=bot_token)
    watcher = ServiceWatcher()

    @client.on(events.NewMessage(pattern="/status"))
    async def handler(event):
        if event.sender_id != int(user_id):
            return

        message = watcher.get_services_status()
        await event.respond(message)

    client.start()
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
