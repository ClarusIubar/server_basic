import http.server
import inspect

print("=== http.server 모듈 전체 탐색 ===\n")

# # 1. 모듈 내부의 모든 것을 출력
# print("1. http.server 모듈 내부 항목들:")
# all_items = dir(http.server)
# for item in all_items[:20]:  # 처음 20개만 출력
#     print(f"   - {item}")
# print(f"   ... 총 {len(all_items)}개의 항목\n")

# # 2. HTTPServer가 뭐지?
# print("2. HTTPServer:")
# print(f"    타입 : {type(http.server.HTTPServer)}")
# print(f"    모듈위치 : {http.server.HTTPServer.__module__}")
# print(f"    소스파일 : {inspect.getfile(http.server.HTTPServer)}\n")

# # 3. HTTPServer의 상속 구조 확인
# print("3. HTTPServer의 상속 구조:")
# print(f"    부모 클래스 : {http.server.HTTPServer.__bases__}")

# # 4. BaseHTTPRequestHandler 분석
# print("4. BaseHTTPRequestHandler 상속 구조:")
# print(f"    부모 클래스 : {http.server.BaseHTTPRequestHandler}")
# print(f"    내부 메서드 일부 : ")
# for method in dir(http.server.BaseHTTPRequestHandler):
#     if method.startswith('do_') or method.startswith('send_'):
#         print(f"    - {method}\n")

# # 5. "from import" vs "import" 비교
# print("5. import 방식 비교")

# # A. 전체 import
# print(" import http.server")
# print(" 사용 : http.server.HTTPserver, http.server.BaseHTTPRequestHandler")
# print(f"    실제주소 : {hex(id(http.server.HTTPServer))}")

# # B. from import
from http.server import HTTPServer as HTTPServer_B, BaseHTTPRequestHandler as Handler_B
# print(" form http.server import HTTPServer, BaseHTTPRequestHandler")
# print(" 사용 : HTTPServer, BaseHTTPRequestHandler")
# print(f"    실제주소 : {hex(id(HTTPServer_B))}")

# 실제로 둘이 같은 객체인지 확인
print("\n6. 두 방식이 가져온 것이 같은 객체인지 확인:")
if http.server.HTTPServer is HTTPServer_B:
    print("   같은 객체입니다! (메모리 주소 동일)")
else:
    print("   다른 객체입니다!")