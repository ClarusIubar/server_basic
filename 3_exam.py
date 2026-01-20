from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import io

# # 분석3 : 실제 응답 문자열 조립해보기
# def build_http_response(status_code, headers, body):
#     """수동으로 HTTP 응답 문자열 조립"""
#     status_message = {
#         200:"OK",
#         404:"Not Found",
#         500:"Internal Server Error"
#     }
#     status_line = f"HTTP/1.1 {status_code}, {status_message.get(status_code, 'Unknwon')}\\r\\n"

#     header_lines = ""
#     for key, value in headers.items():
#         header_lines += f"{key}: {value}\\r\\n"
    
#     empty_line = "\\r\\n"

#     return status_line + header_lines + empty_line + body

# response = build_http_response(
#     200,
#     {'Content-type': "text-html; charset=utf-8"},
#     "<h1>안녕하세요.</h1>"
# )

# print(response)

# 분석6 : 왜 endcode가 필요한가?

text = "<h1>안녕하세요.</h1>"

print(f"    문자열(str): {repr(text)}")
print(f"    타입: {type(text)}")
print()
print(f"    바이트(bytes): {text.encode('utf-8')}")
print(f"    타입: {type(text.encode('utf-8'))}")