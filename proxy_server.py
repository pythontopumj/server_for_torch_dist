import socket
import threading

def forward(source, destination):
    """데이터를 한쪽에서 다른 쪽으로 전달"""
    while True:
        try:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)
        except:
            break
    source.close()
    destination.close()

def handle_worker_connections(master_conn, workers):
    """Master와 모든 Worker 간의 연결을 관리"""
    threads = []
    for worker_conn in workers:
        # Master와 Worker 간 데이터 전달
        threads.append(threading.Thread(target=forward, args=(master_conn, worker_conn)))
        threads.append(threading.Thread(target=forward, args=(worker_conn, master_conn)))
    
    # 모든 스레드 시작
    for thread in threads:
        thread.start()
    
    # 모든 스레드가 종료될 때까지 대기
    for thread in threads:
        thread.join()

def start_proxy_server(host='0.0.0.0', port=44400):
    """프록시 서버 실행"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(10)  # 최대 10개의 연결 허용
    print(f"Listening on port {port}")

    master_conn = None
    workers = []

    try:
        while True:
            # 새로운 연결 수락
            conn, addr = server.accept()
            print(f"Connection established with {addr}")

            # Master 연결이 없는 경우 Master로 설정
            if master_conn is None:
                print("Master connected")
                master_conn = conn
            else:
                print("Worker connected")
                workers.append(conn)

            # Master와 Worker가 연결된 경우 처리 시작
            if master_conn and len(workers) > 0:
                print("Starting communication between Master and Workers...")
                handle_worker_connections(master_conn, workers)

                # Master 연결 종료 또는 유효하지 않은 경우
                print("Resetting connections...")
                master_conn.close()
                for worker_conn in workers:
                    worker_conn.close()

                # 초기 상태로 리셋
                master_conn = None
                workers = []
                print("Ready for new connections...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 서버 종료 시 모든 소켓 닫기
        if master_conn:
            master_conn.close()
        for worker_conn in workers:
            worker_conn.close()
        server.close()


if __name__=="__main__":
    start_proxy_server()