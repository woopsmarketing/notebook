import pygetwindow as gw
import pyautogui
import time

# 카카오톡 창 찾기
windows = gw.getWindowsWithTitle('카카오톡')
if not windows:
    print("KakaoTalk 창을 찾을 수 없습니다.")
    exit()

kakao_window = windows[0]

# 카카오톡 창을 맨 앞으로 가져오기
kakao_window.activate()

# 잠시 대기
time.sleep(1)

# 채팅 목록의 첫 번째 항목 더블 클릭 (위치 조정 필요)
# 첨부된 이미지를 기준으로 채팅방의 위치를 설정합니다.
# 예를 들어, 첫 번째 채팅방의 위치는 다음과 같이 설정할 수 있습니다.
first_chat_x = kakao_window.left + 100
first_chat_y = kakao_window.top + 180

# 첫 번째 채팅방 더블 클릭
pyautogui.doubleClick(first_chat_x, first_chat_y)

print("첫 번째 채팅방에 접속했습니다.")