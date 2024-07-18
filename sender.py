import os
import asyncio
import random
import re
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError, FloodWaitError
from telethon.errors import RPCError

# API 크레덴셜을 환경 변수에서 가져오기
api_id = '21262045'
api_hash = '81d86e68a9ac20bed07aceed72d94065'
session_name = 'session1'

client = None

async def create_client():
    global client
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()
    print(f"Connected client: {session_name}")

async def scrape_groups():
    groups = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            groups.append(dialog.entity.username)
    return groups

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'

async def send_file_with_caption(group_username, image_path, interval):
    await asyncio.sleep(random.randint(5, 30))  # 시작 전에 랜덤 지연 시간 추가

    last_sentence = []
    with open("last_sentence.txt", "r", encoding='UTF-8') as file:
        for line in file:
            last_sentence.append(line.strip())

    message_variations = [
        f'''
        🏆 구글 검색 순위 최상위 (4년 연속 독보적 수행사 1위) 🏆\n\n
        🚀 2024년 3월 최신 구글 알고리즘 반영\n
        🚀 풍부한 작업 경험 보유\n
        🚀 효과적인 백링크와 사이트 분석\n
        🚀 경쟁사 정밀 분석 제공\n
        🚀 국내 구글 검색 순위 최상위 업체 95%가 대행사입니다.\n
        🚀 우리는 직접 수행하는 수행사입니다. (대행사도 우리에게 의뢰)\n\n
        {random.choice(last_sentence)}\n\n
        📢 이 계정은 홍보 전용 계정입니다.\n
        📱 텔레그램 문의: @goat82\n
        📱 텔레그램 문의: @goat82\n
        📱 텔레그램 문의: @goat82\n\n
        ''',
        # 다른 메시지 변형들...
    ]

    message = random.choice(message_variations)

    while True:
        try:
            print(f"이미지 + 메시지 전송 시도 : {group_username}.")
            await client.send_file(group_username, image_path, caption=message)
            print(f"{Color.GREEN}이미지 + 메시지 전송 완료 {group_username} using session: {session_name}{Color.END}")
            await asyncio.sleep(interval)
        except FloodWaitError as e:
            print(f"{Color.YELLOW}FloodWaitError 발생, {e.seconds}초 대기 후 재시도: {group_username}{Color.END}")
            await asyncio.sleep(e.seconds + random.randint(30, 60))
        except RPCError as e:
            await handle_rpc_error(e, group_username, message)
        except Exception as e:
            print(f"{Color.RED}General error sending message to {group_username}: {e}{Color.END}")
            await asyncio.sleep(random.randint(1600, 2000))

async def handle_rpc_error(e, group_username, message):
    error_message = str(e)
    if "CHAT_SEND_PHOTOS_FORBIDDEN" in error_message:
        print(f"{Color.RED}이미지 포함 전송 실패 {group_username}, 메시지만 전송 시도합니다. : {e}{Color.END}")
        await send_message(group_username, message)
    elif "wait" in error_message:
        wait_time_match = re.search(r'wait of (\d+) seconds', error_message)
        if wait_time_match:
            wait_time = int(wait_time_match.group(1)) + random.randint(300, 600)
            print(f"{Color.YELLOW}{wait_time}초 만큼 대기합니다.{Color.END}")
            await asyncio.sleep(wait_time)
        else:
            print(f"{Color.RED}Unexpected wait error format: {error_message}{Color.END}")
            await asyncio.sleep(10)
    else:
        print(f"{Color.RED}Error sending message to {group_username}: {e}{Color.END}")
        await asyncio.sleep(random.randint(1600, 2000))

async def send_message(group_username, message):
    while True:
        try:
            print(f"Attempting to send only message to {group_username}.")
            await client.send_message(group_username, message)
            print(f"{Color.GREEN}메시지만 전송 완료 {group_username} using session: {session_name}{Color.END}")
            await asyncio.sleep(random.randint(1600, 2000))
        except FloodWaitError as e:
            print(f"{Color.YELLOW}FloodWaitError 발생, {e.seconds}초 대기 후 재시도: {group_username}{Color.END}")
            await asyncio.sleep(e.seconds + random.randint(30, 60))
        except RPCError as e:
            await handle_rpc_error(e, group_username, message)
        except Exception as e:
            print(f"{Color.RED}General error sending message to {group_username}: {e}{Color.END}")
            await asyncio.sleep(10)

async def main():
    await create_client()
    try:
        image_path = r'C:\CODE\Telegram\20240716\googletop.png'
        
        # 그룹 방 주소를 스크랩
        groups = await scrape_groups()
        
        # 모든 그룹에 대해 기본 30분 주기로 메시지 전송
        interval = random.randint(1800,2000)  # 30분

        # 병렬로 각 그룹에 메시지 전송
        tasks = [send_file_with_caption(group, image_path, interval) for group in groups]
        await asyncio.gather(*tasks)
    finally:
        await client.disconnect()

if __name__ == "__main__":
    print('10분 쉬고 시작')

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred during the main event loop: {e}")
