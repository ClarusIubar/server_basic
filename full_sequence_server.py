import socket

def start_server():
    # 1. 소켓 생성 및 설정 (TCP/IPv4)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 서버 재시작 시 포트 점유 에러 방지
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 2. 바인딩 및 리스닝 (서버가 포트를 열고 기다리는 단계)
    server.bind(('127.0.0.1', 8000))
    server.listen(5)
    
    print("-" * 50)
    print("Full Sequence Server가 8000번 포트에서 가동 중입니다.")
    print("접속 주소: http://localhost:8000")
    print("-" * 50)

    try:
        while True:
            # 3. 연결 수립 (TCP 3-Way Handshake 완료 후 대화용 소켓 생성)
            client_socket, client_address = server.accept()
            
            # 4. 요청 수신 (클라이언트가 보낸 HTTP 메시지 읽기)
            request_data = client_socket.recv(2048).decode('utf-8')
            if not request_data:
                client_socket.close()
                continue

            # 5. 요청 분석 (Parsing)
            lines = request_data.split('\r\n')
            # 시작 줄 분석: GET /hello HTTP/1.1
            request_line = lines[0]
            method, path, version = request_line.split(' ')
            
            # 헤더에서 User-Agent 추출
            user_agent = "Unknown"
            for line in lines:
                if line.lower().startswith("user-agent:"):
                    user_agent = line.split(": ", 1)[1]
                    break

            print(f"[ACCESS] {method} {path} | From: {client_address}")

            # 6. 로직 처리 (Routing)
            if path == "/":
                status = "200 OK"
                body = "<h1>메인 페이지</h1><p>서버가 당신의 요청을 성공적으로 처리했습니다.</p>"
            elif path == "/hello":
                status = "200 OK"
                body = f"<h1>안녕하세요!</h1><p>당신의 브라우저는 <strong>{user_agent[:50]}...</strong> 이군요.</p>"
            else:
                # 404 상태 코드의 실체 재현
                status = "404 Not Found"
                body = "<h1>404 페이지를 찾을 수 없습니다.</h1>"

            # 7. 응답 메시지 조립 (HTTP Response Structure)
            # (1) 시작 줄
            response = f"HTTP/1.1 {status}\r\n"
            # (2) 응답 헤더
            response += "Content-Type: text/html; charset=utf-8\r\n"
            response += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
            response += "Connection: close\r\n" # 대화 후 연결을 끊겠다는 명시
            # (3) 빈 줄 (Header와 Body의 구분선)
            response += "\r\n"
            # (4) 응답 본문
            response += body

            # 8. 응답 전송 및 연결 종료 (TCP 4-Way Handshake 유도)
            client_socket.send(response.encode('utf-8'))
            client_socket.close() # 서버 측에서 명시적으로 대화 종료

    except KeyboardInterrupt:
        print("\n서버를 안전하게 종료합니다.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()