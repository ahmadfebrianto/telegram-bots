import os
from asyncio import sleep

from telethon import TelegramClient, events


class Service:
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


class Message:
    def build(self, services_status: dict, message_type="status"):
        if message_type == "status":
            message_title = self.__text_bold("Services Status")
            message = f"{message_title}\n\n"
            for service, status in services_status.items():
                if status:
                    message += f"- {service} ::: {self.__text_italic('running')}\n"
                else:
                    message += f"- {service} ::: {self.__text_italic('not running')}\n"

        elif message_type == "alert":
            message_title = self.__text_bold("Services Status Alert")
            message = f"{message_title}\n\n"
            for service, status in services_status.items():
                if not status:
                    message += f"- {service} ::: {self.__text_italic('not running')}\n"

        return message

    def __text_bold(self, text):
        return f"**{text}**"

    def __text_italic(self, text):
        return f"__{text}__"


def main():
    api_id = os.environ.get("TG_API_ID")
    api_hash = os.environ.get("TG_API_HASH")
    bot_token = os.environ.get("TG_BOT_SVCWATCH")
    user_id = os.environ.get("TG_USER_ID")

    client = TelegramClient("svcwatcher", api_id, api_hash).start(bot_token=bot_token)
    watcher = Service()

    @client.on(events.NewMessage(pattern="/status"))
    async def handler(event):
        if event.sender_id != int(user_id):
            return

        message = Message().build(watcher.services_status)
        await event.respond(message)

    @client.on(events.NewMessage(pattern="/start"))
    async def handler(event):
        if event.sender_id != int(user_id):
            return

        while True:
            if watcher.services_status:
                if not all(watcher.services_status.values()):
                    message = Message().build(watcher.services_status, "alert")
            else:
                message = "No services to watch."

            await event.respond(message)
            await sleep(5)

    client.start()
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
