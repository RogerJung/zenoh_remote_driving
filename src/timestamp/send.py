import socket
import time
import datetime

SEND_IP='127.0.0.1'
PORT=12345

def main():
    # Create socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Assign IP address and port
    server_address = (SEND_IP, PORT)
    
    server_socket.connect(server_address)
    
    try:
        while True:
            # Get current timestamp
            current_time = time.time()
            
            # Convert timestamp from "float" to "string"
            # dt_obj = datetime.datetime.fromtimestamp(current_time)
            # time_string = dt_obj.strftime('%H:%M:%S:%f')
            time_string = str(current_time)
            
            # Send timestamp
            server_socket.sendall(time_string.encode())
            print('Send timestamp: %s' % time_string)
            
            time.sleep(1)
    
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
