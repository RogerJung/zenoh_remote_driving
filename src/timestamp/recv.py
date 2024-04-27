import socket
import time

SEND_IP='127.0.0.1'
PORT=12345

def start_server(host, port):
    # 建立 socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 綁定到指定的 IP 位址和通訊埠號
        s.bind((host, port))
        # 最多允許一個連線
        s.listen(1)
        print(f"伺服器正在監聽 {host}:{port}")

        # 等待連線
        conn, addr = s.accept()
        print(f"已建立連線：{addr}")
        while conn:
            # 接收來自客戶端的資料
            data = conn.recv(1024)
            if data:
                timestamp = data.decode()
                # print(f"接收到的 timestamp: {timestamp}")
                f_time = float(timestamp)
                c_time = time.time()
                latency = c_time - f_time
                print(f"latency : {latency} sec")
                
            else:
                print("沒有收到資料")

if __name__ == "__main__":
    start_server(SEND_IP, PORT)
