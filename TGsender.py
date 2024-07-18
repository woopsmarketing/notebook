import os
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError
import asyncio
import random
from telethon.errors import RPCError
import re

# API 크레덴셜을 환경 변수에서 가져오기
api_id = os.getenv('21262045')
api_hash = os.getenv('81d86e68a9ac20bed07aceed72d94065')
session_name = 'session2'

client = None


async def create_client():
    global client
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()
    print(f"Connected client: {session_name}")


class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'


def read_groups(file_path):
    groups = []
    with open(file_path, 'r') as file:
        for line in file:
            groups.append(line.strip().split(',')[0].strip())
    return groups


async def send_file_with_caption(group_username, image_path):
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
        f'''
        🌟 구글 검색 결과 상위 노출 (4년 연속 실적 1위) 🌟\n\n
        🔍 2024년 3월 최신 구글 업데이트 반영\n
        🔍 풍부한 작업 이력 보유\n
        🔍 효과적인 백링크와 사이트 점검\n
        🔍 경쟁사 정밀 분석 제공\n
        🔍 국내 구글 검색 최상위 업체 95%가 대행사입니다.\n
        🔍 우리는 직접 수행하는 실적 회사입니다. (대행사도 우리에게 의뢰)\n\n
        {random.choice(last_sentence)}\n\n
        ⚠️ 이 계정은 홍보 목적으로 사용됩니다.\n
        📞 텔레그램 문의: @goat82\n
        📞 텔레그램 문의: @goat82\n
        📞 텔레그램 문의: @goat82\n\n
        ''',
        f'''
        🏅 구글 상위 노출 (4년 연속 독보적 수행사 1위) 🏅\n\n
        ✅ 2024년 3월 최신 구글 알고리즘 적용\n
        ✅ 작업 이력 풍부\n
        ✅ 효과적인 백링크 및 사이트 진단\n
        ✅ 경쟁업체 정밀 분석\n
        ✅ 국내 구글 상위 노출 업체 95%가 대행사입니다.\n
        ✅ 우리는 직접 수행하는 실행사입니다. (대행사도 우리에게 의뢰)\n\n
        {random.choice(last_sentence)}\n\n
        💡 이 계정은 홍보용 계정입니다.\n
        📱 텔레그램 문의: @goat82\n
        📱 텔레그램 문의: @goat82\n
        📱 텔레그램 문의: @goat82\n\n
        ''',
        f'''
        🔝 구글 검색 상위 노출 (4년 연속 실적 1위) 🔝\n\n
        📈 2024년 3월 구글 최신 업데이트 적용\n
        📈 작업 경력 다수 보유\n
        📈 효과적인 백링크 및 사이트 분석\n
        📈 경쟁사 정밀 분석 서비스 제공\n
        📈 국내 구글 검색 상위 노출 업체 95%가 대행사입니다.\n
        📈 우리는 직접 수행하는 실적 회사입니다. (대행사도 우리에게 의뢰)\n\n
        {random.choice(last_sentence)}\n\n
        📢 이 계정은 홍보 전용 계정입니다.\n
        📞 텔레그램 문의: @goat82\n
        📞 텔레그램 문의: @goat82\n
        📞 텔레그램 문의: @goat82\n\n
        '''
    ]

    message = random.choice(message_variations)

    while True:
        try:
            print(f"이미지 + 메시지 전송 시도 : {group_username}.")
            await client.send_file(group_username, image_path, caption=message)
            print(f"{Color.GREEN}이미지 + 메시지 전송 완료 {group_username} using session: {session_name}{Color.END}")
            await asyncio.sleep(random.randint(1600, 2000))  # 기본 대기 시간
        except RPCError as e:
            await handle_rpc_error(e, group_username, message)
        except Exception as e:
            print(f"{Color.RED}General error sending message to {group_username}: {e}{Color.END}")
            await asyncio.sleep(random.randint(1600, 2000))


async def send_message(group_username, message):
    while True:
        try:
            print(f"Attempting to send only message to {group_username}.")
            await client.send_message(group_username, message)
            print(f"{Color.GREEN}메시지만 전송 완료 {group_username} using session: {session_name}{Color.END}")
            await asyncio.sleep(random.randint(1600, 2000))
        except RPCError as e:
            await handle_rpc_error(e, group_username, message)
        except Exception as e:
            print(f"{Color.RED}General error sending message to {group_username}: {e}{Color.END}")
            await asyncio.sleep(10)


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


async def main():
    await create_client()
    try:
        image_path = r'C:\Users\woops\project\pyrogram\mytelegram\googletop.png'
        group_file = "group2.txt"  # 단일 그룹 파일 사용

        groups = read_groups(group_file)

        tasks = [send_file_with_caption(group, image_path) for group in groups]
        await asyncio.gather(*tasks)
    finally:
        await client.disconnect()

if __name__ == "__main__":
    print('10분쉬고 시작')

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred during the main event loop: {e}")