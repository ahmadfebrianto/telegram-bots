import os
from asyncio import sleep

from telethon import TelegramClient, events


class ServiceWatcher:
    @property
    def service_list(self):
        with open("services.txt") as f:
            # Parse comments and empty lines
            services = [
                line.strip()
                for line in f.readlines()
                if line.strip() and not line.strip().startswith("#")
            ]

            return services

    @property
    def services_status(self):
        if not self.service_list:
            return None

        _services_status = {}
        for service in self.service_list:
            _services_status[service] = self.is_service_running(service)

        return _services_status

    @staticmethod
    def is_service_running(service_name):
        status = os.system(f"systemctl is-active --quiet {service_name}")
        return status == 0

    def build_message(self, _type="status"):
        if not self.services_status:
            return "No services to watch."

        if _type == "status":
            message_title = "**Services Status**"
            message = f"{message_title}\n\n"
            for service, status in self.services_status.items():
                message += f"- {service} ::: {'__running__' if status else '__not running__'}\n"

        elif _type == "alert":
            message_title = "**Services Alert**"
            message = f"{message_title}\n\n"
            for service, status in self.services_status.items():
                if not status:
                    message += f"- {service} ::: __not running__\n"

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

        message = watcher.build_message()
        await event.respond(message)

    @client.on(events.NewMessage(pattern="/start"))
    async def handler(event):
        if event.sender_id != int(user_id):
            return

        while True:
            if watcher.services_status:
                if not all(watcher.services_status.values()):
                    message = watcher.build_message(_type="alert")
            else:
                message = watcher.build_message()

            await event.respond(message)
            await sleep(5)

    client.start()
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
