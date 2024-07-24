import socks
import socket
import urllib.request

# 프록시 설정
proxy_host = 'brd.superproxy.io'
proxy_port = 22225
proxy_username = 'brd-customer-hl_62a3bae9-zone-seattle'
proxy_password = 'y1szgxcybgz1'

# socks 프록시 설정
socks.set_default_proxy(socks.HTTP, proxy_host, proxy_port, True, proxy_username, proxy_password)
socket.socket = socks.socksocket

# 테스트 URL
url = 'http://www.httpbin.org/ip'

# 프록시를 통해 URL에 접속
response = urllib.request.urlopen(url)
print(response.read().decode('utf-8'))