import socket

def run_ua_check_server():
    # 1. 소켓 설정 및 포트 바인딩
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 서버 재시작 시 발생할 수 있는 'Address already in use' 에러 방지
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server.bind(('127.0.0.1', 8000))
    server.listen(1)
    
    print("=" * 50)
    print("User-Agent 판별 서버가 8000번 포트에서 가동 중입니다.")
    print("크롬, 엣지 등 서로 다른 브라우저로 접속하여 결과를 비교해 보세요.")
    print("=" * 50)

    try:
        while True:
            client, addr = server.accept()
            raw_request = client.recv(2048).decode('utf-8')
            
            if not raw_request:
                client.close()
                continue

            # 2. HTTP 요청 헤더에서 User-Agent 추출
            lines = raw_request.split('\r\n')
            user_agent = ""
            for line in lines:
                if line.lower().startswith("user-agent:"):
                    user_agent = line
                    break

            # 3. 브라우저 엔진 및 이름 판별 (질적 변화 확인)
            # 엣지는 'Edg'라는 문자열을 포함하므로 크롬보다 먼저 체크해야 정확합니다.
            if "Edg" in user_agent:
                browser_name = "Microsoft Edge"
                msg = "엣지(Edge) 브라우저를 사용 중이시군요! 깔끔한 속도가 장점이죠."
            elif "Chrome" in user_agent:
                browser_name = "Google Chrome"
                msg = "크롬(Chrome) 브라우저를 사용 중이시군요! 가장 대중적인 선택입니다."
            elif "Firefox" in user_agent:
                browser_name = "Mozilla Firefox"
                msg = "파이어폭스(Firefox)를 사용 중이시군요! 개인정보 보호에 탁월합니다."
            else:
                browser_name = "Unknown Browser"
                msg = "새로운 환경 혹은 모바일에서 접속하셨네요. 반갑습니다!"

            print(f"[{addr}] 접속 감지 | 판별된 브라우저: {browser_name}")

            # 4. 맞춤형 HTML 응답 생성
            response_body = f"""
            <html>
                <head><meta charset="utf-8"></head>
                <body>
                    <h1>브라우저 식별 결과</h1>
                    <p style="font-size: 1.2em; color: blue;"><strong>{msg}</strong></p>
                    <hr>
                    <p><strong>서버가 읽은 당신의 User-Agent:</strong></p>
                    <code style="background: #f4f4f4; padding: 10px; display: block;">{user_agent}</code>
                </body>
            </html>
            """

            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: text/html; charset=utf-8\r\n"
            response += f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
            response += "\r\n"
            response += response_body

            client.send(response.encode('utf-8'))
            client.close()

    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")
    finally:
        server.close()

if __name__ == "__main__":
    run_ua_check_server()