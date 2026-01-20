import socket
import traceback
import json

def start_debug_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8000))
    server.listen(5)
    
    print("=" * 70)
    print(" [브라우저 콘솔 디버깅 서버] http://localhost:8000/error 접속")
    print("=" * 70)

    try:
        while True:
            client_socket, client_address = server.accept()
            request_data = client_socket.recv(4096).decode('utf-8')
            if not request_data:
                client_socket.close()
                continue

            path = request_data.split('\n')[0].split(' ')[1]

            try:
                if path == "/":
                    status = "200 OK"
                    body = "<h1>정상 페이지</h1><p>/error로 가서 F12를 누르세요.</p>"
                elif path == "/error":
                    # 의도적 에러: 정의되지 않은 변수 참조
                    print(f"[!] {client_address}에서 에러 유발 경로 접속")
                    result = undefined_variable + 10 
                    status = "200 OK"
                    body = "성공"
                else:
                    status = "404 Not Found"
                    body = "404"

            except Exception as e:
                status = "500 Internal Server Error"
                # 에러의 전체 경로와 내용을 문자열로 추출
                error_detail = traceback.format_exc()
                
                # 자바스크립트 문자열 깨짐 방지를 위한 처리 (JSON 인코딩 활용)
                safe_error_msg = json.dumps(error_detail)
                
                # 브라우저 콘솔에 에러를 출력하는 JS 코드를 바디에 담음
                body = f"""
                <html>
                    <body>
                        <h1 style="color:red;">500 Internal Server Error</h1>
                        <p>서버 에러가 발생했습니다. <b>F12를 눌러 콘솔(Console) 탭을 확인하세요.</b></p>
                        <script>
                            console.error("--- SERVER SIDE ERROR LOG ---");
                            console.error({safe_error_msg});
                        </script>
                    </body>
                </html>
                """

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
    start_debug_server()