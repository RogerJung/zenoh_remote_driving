import socket
import time

SEND_IP='127.0.0.1'
PORT=12345

def start_server(host, port):
    # Create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Server listening at {host}:{port}")

        # Waiting connection
        conn, addr = s.accept()
        print(f"Establish connection: {addr}")
        while conn:
            # Recv client's date
            data = conn.recv(1024)
            if data:
                timestamp = data.decode()

                f_time = float(timestamp)
                c_time = time.time()
                latency = c_time - f_time
                print(f"latency : {latency} sec")
                
if __name__ == "__main__":
    start_server(SEND_IP, PORT)
