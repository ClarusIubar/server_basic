from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable, Optional
from socketserver import BaseServer
import inspect

print("--- 클래스 방식 or 함수방식 ---\\n")

print("[원본] 클래스 방식:\\n")
# ============================================================
# [원본] 클래스 방식 (기존 코드)
# ============================================================
class MyRequestHander_Class(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        msg = "<h1>안녕하세요! [클래스 방식] 서버 입니다.<h1>"
        self.wfile.write(msg.encode('utf-8'))

def run_server_class():
    server = HTTPServer(('localhost', 8000), MyRequestHander_Class)
    print(" - 클래스로 do_GET 메서드 오버라이딩")
    print(" - HTTPServer에 핸들러 클래스 전략 패턴 전달")
    print(" - HTTPServer가 요청할 때 마다 인스턴스 생성(팩토리)")
    return server

# ============================================================
# [변형 1] 함수를 직접 할당하는 방식
# ============================================================
# print("【변형 1】함수를 직접 할당하는 방식:\\n")

# def my_hander_function(request, client_address, server):
#         """HTTPServer는 요청 처리 함수를 기대하지 않고 Handler 클래스를 기대함"""
#     pass

# class HandlerWithFunction(BaseHTTPRequestHandler):
#     # handler_function = None
#     handler_function: Optional[Callable] = None

#     def do_GET(self):
#         if self.handler_function:
#             self.handler_function(self)
#         else:
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html; charset=utf-8')
#             self.end_headers()
#             msg  = "<h1>함수가 설정되지 않음</h1>"
#             self.wfile.write(msg.encode('utf-8'))

# def my_response_function(handler):
#     handler.send_response(200)
#     handler.send_header('Content-type', 'text/html; charset=utf-8')
#     handler.end_headers()
#     message = "<h1>안녕하세요! [함수 방식] 서버입니다.</h1>"
#     handler.wfile.write(message.encode('utf-8'))

# # 올바른 할당 방식: 함수 이름만 대입 (괄호 없이)
# HandlerWithFunction.handler_function = my_response_function

# ============================================================
# [변형 2] lambda 함수 사용
# ============================================================
print("【변형 2】lambda 함수 사용:\\n")

class HandlerWithLambda(BaseHTTPRequestHandler):
    do_GET = lambda self: (
        self.send_response(200),
        self.send_header('Content-type', 'text/html; charset=utf-8'),
        self.end_headers(),
        self.wfile.write("<h1>안녕하세요! [Lambda] 서버입니다.</h1>".encode('utf-8'))
    )

# ============================================================
# [변형 3] 함수로 Handler 클래스 동적 생성
# ============================================================
print("【변형 3】함수로 Handler 동적 생성:\\n")

def create_handler_class(response_message):
    """함수가 실행될 때마다 새로운 Handler 클래스를 반환"""
    class DynamicHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(response_message.encode('utf-8'))
    return DynamicHandler

Handler1 = create_handler_class("<h1>서버 1입니다.</h1>")
Handler2 = create_handler_class("<h1>서버 2입니다.</h1>")

# ============================================================
# [변형 4] 완전히 절차적인 방식 (if-else 체인)
# ============================================================
print("【변형 4】완전 절차적 스타일 (if-else 체인):\\n")

class ProceduralHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path

        if path == '/':
            response_data = "<h1>메인 페이지</h1>"
        elif path == '/about':
            response_data = "<h1>소개 페이지</h1>"
        elif path == '/contact':
            response_data = "<h1>연락처 페이지</h1>"
        else:
            response_data = "<h1>404 - 페이지를 찾을 수 없음</h1>"

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(response_data.encode('utf-8'))