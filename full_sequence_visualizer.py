import socket

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8000))
    server.listen(5)
    
    print("=" * 70)
    print(" [시스템 모니터링 시작] http://localhost:8000 접속을 기다립니다.")
    print(" 이 터미널에서는 브라우저와 서버 간의 '날것의 대화'가 실시간 출력됩니다.")
    print("=" * 70)

    try:
        while True:
            # 1. 연결 수립
            client_socket, client_address = server.accept()
            
            # 2. 요청 수신 및 터미널 출력
            request_data = client_socket.recv(4096).decode('utf-8')
            if not request_data:
                client_socket.close()
                continue

            print("\n" + ">>> [1. 클라이언트의 요청 전문] " + "-" * 40)
            print(request_data) 

            # 3. 요청 분석 (Parsing)
            lines = request_data.split('\r\n')
            request_line = lines[0]
            method, path, version = request_line.split(' ')
            
            # 4. 로직 처리 및 응답 본문(Body) 생성
            # 웹 화면에서도 전체 과정을 볼 수 있도록 본문에 정보를 담습니다.
            status = "200 OK"
            if path == "/favicon.ico":
                client_socket.close()
                continue

            # 웹 브라우저 화면에 표시될 HTML 내용
            body_content = f"""
            <html>
                <head><meta charset="utf-8"><title>HTTP 시퀀스 확인</title></head>
                <body style="font-family: monospace; line-height: 1.5; padding: 20px; background-color: #f8f9fa;">
                    <h1 style="color: #d93025;">[웹 브라우저 수신 결과]</h1>
                    <div style="background: #e8f0fe; border: 1px solid #1a73e8; padding: 15px; border-radius: 5px;">
                        <h3>1. 분석된 요청 정보</h3>
                        <ul>
                            <li><b>Method:</b> {method}</li>
                            <li><b>Path:</b> {path}</li>
                            <li><b>Protocol:</b> {version}</li>
                            <li><b>From:</b> {client_address}</li>
                        </ul>
                    </div>
                    <br>
                    <div style="background: #fff; border: 1px solid #ccc; padding: 15px; border-radius: 5px;">
                        <h3>2. 서버가 당신에게 보낸 응답 전문 (Raw Response)</h3>
                        <pre style="white-space: pre-wrap; word-wrap: break-word; color: #333;">
"""
            # 응답 메시지 조립
            status_line = f"HTTP/1.1 {status}\r\n"
            headers = "Content-Type: text/html; charset=utf-8\r\n"
            headers += "Connection: close\r\n"
            
            # 임시 본문 완성 (전문 확인용)
            full_body_start = body_content
            full_body_end = "\n</pre></div></body></html>"
            
            # 전체 응답 텍스트 미리 계산 (화면 표시용)
            mock_response_text = status_line + headers + "\r\n" + "[HTML 본문 데이터 생략...]"
            
            # 최종 본문 합치기
            final_body = full_body_start + mock_response_text + full_body_end
            
            # 실제 헤더에 정확한 Content-Length 반영
            headers += f"Content-Length: {len(final_body.encode('utf-8'))}\r\n"
            
            # 최종 패키지 조립
            full_response = status_line + headers + "\r\n" + final_body

            # 5. 응답 전송 정보 터미널 출력
            print("\n" + "<<< [2. 서버의 응답 전문] " + "-" * 42)
            print(full_response)
            print("-" * 70)

            # 6. 전송 및 종료
            client_socket.send(full_response.encode('utf-8'))
            client_socket.close()

    except KeyboardInterrupt:
        print("\n서버 모니터링을 종료합니다.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()