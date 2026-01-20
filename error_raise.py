import socket
import traceback

def start_error_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8000))
    server.listen(5)
    
    print("=" * 70)
    print(" [500 에러 재현 서버] http://localhost:8000/error 에 접속하세요.")
    print("=" * 70)

    try:
        while True:
            client_socket, client_address = server.accept()
            request_data = client_socket.recv(4096).decode('utf-8')
            if not request_data:
                client_socket.close()
                continue

            lines = request_data.split('\r\n')
            path = lines[0].split(' ')[1]

            try:
                # [정상 로직]
                if path == "/":
                    status = "200 OK"
                    body = "<h1>정상 페이지입니다.</h1><p>/error 로 접속해 보세요.</p>"
                
                # [500 에러 유도 로직]
                elif path == "/error":
                    print("\n[!] 의도적인 서버 내부 오류 발생 중...")
                    # 0으로 나누기 오류 (ZeroDivisionError) 강제 발생
                    result = 10 / 0 
                    status = "200 OK" # 여기까지 도달하지 못함
                    body = f"결과: {result}"

                else:
                    status = "404 Not Found"
                    body = "<h1>404 Not Found</h1>"

            except Exception as e:
                # 서버 내부에서 에러가 발생했을 때 수행되는 블록
                status = "500 Internal Server Error"
                error_detail = traceback.format_exc() # 에러의 상세 내용(Stack Trace)
                print(f"\n[ERROR 500] 서버 내부 예외 발생:\n{error_detail}")
                
                body = f"""
                <html>
                    <body style="font-family: sans-serif; padding: 20px; color: #721c24; background-color: #f8d7da;">
                        <h1>500 Internal Server Error</h1>
                        <p>서버 내부에서 파이썬 코드가 폭발했습니다!</p>
                        <hr>
                        <h3>에러 원인:</h3>
                        <pre style="background: #fff; padding: 10px; border: 1px solid #f5c6cb;">{e}</pre>
                    </body>
                </html>
                """

            # 응답 조립 및 전송
            response = f"HTTP/1.1 {status}\r\n"
            response += "Content-Type: text/html; charset=utf-8\r\n"
            response += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
            response += "Connection: close\r\n\r\n"
            response += body

            client_socket.send(response.encode('utf-8'))
            client_socket.close()

    except KeyboardInterrupt:
        print("\n서버 종료")
    finally:
        server.close()

if __name__ == "__main__":
    start_error_server()