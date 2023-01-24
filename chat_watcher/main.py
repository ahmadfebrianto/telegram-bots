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


async def get_group_ids(client):
    group_ids = []
    async for dialog in client.iter_dialogs():
        group_and_id = f"{dialog.name} {dialog.id}"
        group_ids.append(group_and_id)

    return group_ids


def main():

    api_id = os.environ.get("TG_API_ID")
    api_hash = os.environ.get("TG_API_HASH")
    client = TelegramClient("chatwatcher", api_id, api_hash)

    # Patterns to watch for
    patterns_filename = "patterns.txt"
    patterns = read_file(patterns_filename)

    # Groups to watch
    group_ids_filename = "group_ids.txt"
    group_ids = [int(group_id) for group_id in read_file(group_ids_filename)]

    @client.on(events.NewMessage(chats=group_ids))
    async def new_message_handler(event):
        text = event.raw_text
        for pattern in patterns:
            match = re.search(r"" + pattern, text, re.IGNORECASE)
            if match:
                message = (
                    f"{text}"
                    f"\n\n"
                    f"https://t.me/c/{event.chat.id}/{event.message.id}"
                )
                await client.send_message("me", message)
                break

    client.start()

    # Create a file with groups and their IDs
    groups_and_ids_filename = "groups_and_ids.txt"
    if not os.path.exists(groups_and_ids_filename):
        group_ids = client.loop.run_until_complete(get_group_ids(client))
        with open(groups_and_ids_filename, "w") as f:
            f.write("\n".join(group_ids))

    client.run_until_disconnected()


if __name__ == "__main__":
    main()
