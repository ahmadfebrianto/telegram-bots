import os
from asyncio import sleep

from telethon import TelegramClient, events


class Service:
    @property
    def list(self):
        with open("services.txt") as f:
            # Parse comments and empty lines
            services = [
                line.strip()
                for line in f.readlines()
                if line.strip() and not line.strip().startswith("#")
            ]

            return services

    @property
    def status(self):
        if not self.list:
            return None

        _services_status = {}
        for service in self.list:
            _services_status[service] = self.is_service_running(service)

        return _services_status

    @staticmethod
    def is_service_running(service_name):
        status = os.system(f"systemctl is-active --quiet {service_name}")
        return status == 0


class Message:
    def __new__(cls, services_status, message_type="status") -> str:
        instance = super().__new__(cls)
        instance.services_status = services_status
        instance.message_type = message_type
        return instance.__build()

    def __build(self):
        if self.message_type == "status":
            message_title = self.__text_bold("Services Status")
            message = f"{message_title}\n\n"
            for service, status in self.services_status.items():
                if status:
                    message += f"- {service} ::: {self.__text_italic('running')}\n"
                else:
                    message += f"- {service} ::: {self.__text_italic('not running')}\n"

        elif self.message_type == "alert":
            message_title = self.__text_bold("Services Status Alert")
            message = f"{message_title}\n\n"
            for service, status in self.services_status.items():
                if not status:
                    message += f"- {service} ::: {self.__text_italic('not running')}\n"

        return message

    def __text_bold(self, text):
        return f"**{text}**"

    def __text_italic(self, text):
        return f"__{text}__"


class Bot:
    def __init__(self) -> None:
        api_id = os.environ.get("TG_API_ID")
        api_hash = os.environ.get("TG_API_HASH")
        bot_token = os.environ.get("TG_BOT_SVCWATCH")

        self.user_id = os.environ.get("TG_USER_ID")

        self.client = TelegramClient("svcwatcher", api_id, api_hash).start(
            bot_token=bot_token
        )
        self.service = Service()
        self.running = False

    async def on_status(self, event):
        if event.sender_id != int(self.user_id):
            return

        message = Message(self.service.status)
        await event.respond(message)

    async def on_start(self, event):
        if event.sender_id != int(self.user_id):
            return

        if self.running:
            await event.respond("Watcher is already running.")
            return

        self.running = True

        while True:
            if self.service.status:
                if not all(self.service.status.values()):
                    message = Message(self.service.status, "alert")
                    await event.respond(message)
            else:
                message = "No services to watch."
                await event.respond(message)

            await sleep(5)

    def start(self):
        self.client.add_event_handler(
            self.on_status, events.NewMessage(pattern="/status")
        )
        self.client.add_event_handler(
            self.on_start, events.NewMessage(pattern="/start")
        )
        self.client.start()
        self.client.run_until_disconnected()


if __name__ == "__main__":
    bot = Bot()
    bot.start()

# UnboundLocalError: local variable 'message' referenced before assignment
