import socket

# 8000번 포트에서 대기하는 서버 설정
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8000))
server.listen(1)

print("서버 실행 중... 브라우저 주소창에 'localhost:8000'을 입력하고 엔터를 누르세요.")

while True:
    client, addr = server.accept()
    # 브라우저가 보낸 데이터를 읽음
    request = client.recv(1024).decode('utf-8')
    
    print("-" * 30)
    print(f"클라이언트 접속: {addr}")
    print("브라우저가 보낸 요청 내용:")
    print(request) # 이 부분이 핵심입니다.
    print("-" * 30)

    # 브라우저에게 보내는 응답 (HTML)
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    response += "<h1>Hello! 연결에 성공했습니다.</h1>"
    
    client.send(response.encode('utf-8'))
    client.close()