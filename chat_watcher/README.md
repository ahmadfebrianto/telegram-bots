# Chat Watcher

A simple bot that watches for messages in a Telegram chat or groups you are in. If it detects a message with a specific keyword, it will copy the message to `Saved Messages`.

## Setup

1. Install telethon

   ```bash
   pip install telethon
   ```

2. Create a new Telegram application and get the API ID and API hash. Save them in an environment variable called `TG_API_ID` and `TG_API_HASH` respectively. To do this, go to [my.telegram.org](https://my.telegram.org/auth) and create a new application.

3. Add the keywords to watch in `patterns.txt`. Each keyword should be in regex format and on a new line. Each message is checked against all the keywords sequentially. If a message matches any of the keywords, it will be copied to `Saved Messages`.

4. Add group IDs to watch in `group_ids.txt`. To get the IDs of all the groups you are in, run the script once. It will generate a file named `groups_and_ids.txt` in the same directory. Copy the IDs of the groups you want to watch and paste them in `group_ids.txt`. Each group ID should be on a new line. You can also add a comment after the ID by adding a `#` and then the comment.

5. Run the script

   ```bash
   python3 main.py
   ```

## Special notes

- This bot can be used to copy certain messages from a group where the `forward feature` is `disabled`.
- This bot acts on your behalf. That means not bot (created by BotFather) is required to be added to the group. It will work even if you are not an admin in the group.
