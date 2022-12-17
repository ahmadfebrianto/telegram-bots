import os
import re

from telethon import TelegramClient, events


def read_file(filename):
    with open(filename) as f:
        container = []
        for line in f:
            if not line.startswith("#"):
                group_id = line.split("#")[0]
                container.append(group_id.strip())

        return container


def main():

    api_id = os.environ.get("TG_API_ID")
    api_hash = os.environ.get("TG_API_HASH")
    client = TelegramClient("chatwatcher", api_id, api_hash)

    # Patterns to watch for
    patterns_filename = "patterns.txt"
    patterns = read_file(patterns_filename)

    # Groups to watch
    group_ids_filename = "groups.txt"
    group_ids = [int(group_id) for group_id in read_file(group_ids_filename)]

    @client.on(events.NewMessage(chats=group_ids))
    async def new_message_handler(event):
        text = event.raw_text
        for pattern in patterns:
            match = re.search(r"" + pattern, text, re.IGNORECASE)
            if match:
                await client.send_message("me", text)
                break

    client.start()
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
