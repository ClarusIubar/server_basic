import socket
import threading
import time

def run_server():
    # 8000번 포트를 사용하는 서버 생성
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8000))
    server.listen(1)
    print("[Server] 8000번 포트에서 대기 중...")
    
    conn, addr = server.accept()
    print(f"[Server] {addr}로부터 연결됨.")
    conn.close()
    server.close()

def run_client(target_port):
    time.sleep(1) # 서버가 켜질 때까지 잠시 대기
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[Client] {target_port}번 포트로 접속 시도 중...")
    
    try:
        client.connect(('127.0.0.1', target_port))
        print(f"[Client] {target_port}번 접속 성공!")
    except ConnectionRefusedError:
        print(f"[Client] 접속 실패: Connection Refused (포트 {target_port}가 닫혀 있음)")
    except Exception as e:
        print(f"[Client] 기타 에러: {e}")
    finally:
        client.close()

# 테스트 실행
if __name__ == "__main__":
    # 서버는 8000번으로 실행
    threading.Thread(target=run_server, daemon=True).start()
    
    # 클라이언트는 8001번으로 접속 시도 (실패 케이스)
    run_client(8001)
    
    # 클라이언트는 8000번으로 접속 시도 (성공 케이스)
    run_client(8000)