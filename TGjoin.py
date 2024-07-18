import re
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import FloodWaitError
from datetime import datetime
import random


api_id = '21262045'
api_hash = '81d86e68a9ac20bed07aceed72d94065'

group_links_file = 'unformatted_text.txt'
# Regular expression pattern to match URLs
pattern = r'(https?://\S+)'


async def join_group(client, group_link):
    try:
        await client(JoinChannelRequest(group_link))
        print(f"Joined the group: {group_link}")

    except FloodWaitError as e:
        print(
            f"Error joining group {group_link}: A wait of {e.seconds} seconds is required")
        await asyncio.sleep(e.seconds + random.randint(30, 60))
        # FloodWaitError가 발생했을 때 재시도합니다.
        await join_group(client, group_link)
    except Exception as e:
        print(f"Error joining group {group_link}: {e}")


async def extract_links_and_save_to_file(unformatted_text_file):
    # Read unformatted text containing links from the file
    group_links = []
    try:
        with open(unformatted_text_file, 'r', encoding='utf-8') as file:
            text = file.read()
            # Find all URLs in the text using the regex pattern
            links = re.findall(pattern, text)
            # Write the extracted links to a text file
            with open('group_links.txt', 'w') as output_file:
                for link in links:
                    output_file.write(link + '\n')
        print("Links extracted and saved to 'group_links.txt' file.")
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}. Skipping the line.")


async def join_groups_from_file(group_links_file):
    session_id = 'session1'
    # Read group links from the text file with UTF-8 encoding
    with open(group_links_file, 'r', encoding='utf-8') as file:
        group_links = [line.strip() for line in file.readlines()]

    async with TelegramClient(session_id, api_id, api_hash) as client:
        for group_link in group_links:
            try:
                await join_group(client, group_link)
                # Add a 30 to 60 seconds delay between joining each chat
                await asyncio.sleep(random.randint(30, 60))
                now = datetime.now()
                print("문자열 변환 : ", now.strftime('%Y-%m-%d %H:%M:%S'))
            except FloodWaitError:
                print(
                    f"Flood wait error on {group_link}, retrying after delay.")
                await asyncio.sleep(random.randint(30, 60))


async def main():
    # Run the asyncio event loop to extract links and save to file
    # await extract_links_and_save_to_file(group_links_file)
    # Run the asyncio event loop to join groups from file
    await join_groups_from_file('group_links.txt')


if __name__ == "__main__":
    asyncio.run(main())
