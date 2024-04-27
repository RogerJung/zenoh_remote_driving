import socket
import time
import datetime

SEND_IP='127.0.0.1'
PORT=12345

def main():
    # 建立一個 socket 物件
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 連線的 IP 位址和埠號
    server_address = (SEND_IP, PORT)
    
    print('連線至 %s 的埠號 %s' % server_address)
    
    # 連線至伺服器
    server_socket.connect(server_address)
    
    try:
        while True:
            # 獲取當前時間戳
            current_time = time.time()
            
            # 將時間戳轉換為字串
            # dt_obj = datetime.datetime.fromtimestamp(current_time)
            # time_string = dt_obj.strftime('%H:%M:%S:%f')
            time_string = str(current_time)
            
            # 將時間戳發送至伺服器
            server_socket.sendall(time_string.encode())
            print('已發送時間戳：%s' % time_string)
            
            
            # 等待一段時間再繼續下一個迴圈
            time.sleep(1)
    
    finally:
        # 結束連線
        print('關閉 socket 連線')
        server_socket.close()

if __name__ == '__main__':
    main()
