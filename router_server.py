import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 포트 재사용 설정 (서버 재시작 시 'Address already in use' 방지)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 8000))
server.listen(1)

print("서버 실행 중... 'localhost:8000' 또는 'localhost:8000/hello'에 접속하세요.")

while True:
    client, addr = server.accept()
    raw_request = client.recv(1024).decode('utf-8')
    
    if not raw_request:
        client.close()
        continue

    # 1. 요청의 첫 줄 추출 및 분석
    request_line = raw_request.split('\r\n')[0]
    method, path, version = request_line.split(' ')
    
    print(f"[{method}] 경로 요청됨: {path}")

    # 2. 경로(Path)에 따른 조건부 응답 처리 (Routing)
    if path == "/":
        response_body = "<h1>메인 페이지입니다.</h1><p>주소창 뒤에 /hello를 붙여보세요.</p>"
    elif path == "/hello":
        response_body = "<h1>안녕하세요!</h1><p>특정 경로로의 접속을 환영합니다.</p>"
    elif path == "/favicon.ico":
        # 파비콘 요청은 로그만 남기고 본문은 비움
        response_body = ""
    else:
        # 약속되지 않은 경로로 들어왔을 때 (404 Not Found의 실체)
        response_body = "<h1>404 찾을 수 없음</h1><p>존재하지 않는 페이지입니다.</p>"

    # 3. HTTP 응답 생성 및 전송
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    response += response_body
    
    client.send(response.encode('utf-8'))
    client.close()