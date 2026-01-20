from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import os
import sys

# # 방법1 : 튜플로 전달
# host_port_tuple = ('localhost', 8000)
# print(" server = HTTPServer(host_port_tuple, simpleHandler)")
# print()
# print("튜플 분해:")
# print(f"    host: {host_port_tuple[0]}")
# print(f"    host: {host_port_tuple[1]}")
# print(f"    타입: {type(host_port_tuple)}")
# print(f"    길이: {len(host_port_tuple)}")
# print()

# # 방법2 : 별도 변수 사용
# host = 'localhost'
# port = 8000

# print("   host = 'localhost'")
# print("   port = 8000")
# print(" server = HTTPServer((host, port), simpleHandler)")
# print()
# print(" 장점:")
# print("   - 변수 이름으로 의미 명확")
# print("   - 재사용 가능")
# print("   - 쉽게 수정 가능")
# print()

# 방법3 : 환경 변수 사용

# env_host = os.environ.get('SERVER_HOST', 'localhost')
# env_port = int(os.environ.get('SERVER_PORT', '8000'))

# print("코드:")
# print("   import os")
# print("   host = os.environ.get('SERVER_HOST', 'localhost')")
# print("   port = int(os.environ.get('SERVER_PORT', '8000'))")
# print()
# print("장점:")
# print("   - 실행 환경마다 다른 설정 가능")
# print("   - 코드 수정 없이 설정 변경")
# print("   - 배포/개발 환경 분리")
# print()

# # 방법4 : 명령줄 인자
# def parse_args(args):
#     host = 'localhost'
#     port = 8000

#     for arg in args[1:]:
#         if arg.startswith('--host='):
#             host = arg.split('=')[1]
#         elif arg.startswith('--port='):
#             port = int(arg.split('=')[1])

#     return host, port

# test_args = ['server.py', '--host=127.0.0.1', '--port=9000']
# cli_host, cli_port = parse_args(test_args)

# print("코드:")
# print("   import sys")
# print("   def parse_args(argv): ...")
# print("   host, port = parse_args(sys.argv)")
# print()
# print(f"테스트: {test_args}")
# print(f"결과: host={cli_host}, port={cli_port}")
# print()

# 방법5 : 설정파일(JSON)

# import json
# config_json = """
# {
#     "server":{
#         "host":"localhost",
#         "port": 8000
#     }
# }
# """

# config = json.loads(config_json)
# config_host = config['server']['host']
# config_port = config['server']['port']

# print("config.json 파일:")
# print(config_json)
# print()
# print("코드:")
# print("   import json")
# print("   host = config['server']['host']")
# print("   port = config['server']['port']")
# print()

# 방법7: 다양한 호스트 설정
host_examples = [
    ("localhost", "로컬호스트 (자기 컴퓨터)"),
    ("127.0.0.1", "IPv4 루프백 주소"),
    ("0.0.0.0", "모든 네트워크 인터페이스 (외부 접속 허용)")
]

print("호스트 옵션들:")
for host, desc in host_examples:
    print(f"   '{host}' → {desc}")
print()