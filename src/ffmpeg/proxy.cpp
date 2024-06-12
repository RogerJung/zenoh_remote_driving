#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include <cstdlib>

using namespace std;

#define MAX_BUFFER_SIZE 8192
#define PORT_A 8003 // Input port
#define PORT_B 8080 // Output port

int main() {

    const char *VEHICLE_IP = getenv("VEHICLE_IP");
    string env_var(VEHICLE_IP ? VEHICLE_IP : "");
    if (env_var.empty()) {
        cerr << "[ERROR] No such variable found!" << endl;
        exit(EXIT_FAILURE);
    }

    cout << "VEHICLE_IP : " << env_var << endl;

    // Create first socket
    int sockfd_a = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd_a < 0) {
        std::cerr << "Error: Couldn't create socket A." << std::endl;
        return -1;
    }

    // Create second socket
    int sockfd_b = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd_b < 0) {
        std::cerr << "Error: Couldn't create socket B." << std::endl;
        return -1;
    }

    int enable = 1;
    if (setsockopt(sockfd_a, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(enable)) == -1) {
        std::cerr << "Error: Couldn;t set socket A reused." << std::endl;
        return -1;
    }

    if (setsockopt(sockfd_b, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(enable)) == -1) {
        std::cerr << "Error: Couldn;t set socket B reused." << std::endl;
        return -1;
    }

    // Set socket priority to second socket
    int optval =  0;
    if(setsockopt(sockfd_b, SOL_SOCKET, SO_PRIORITY, &optval, sizeof(optval)) < 0){
        printf("Fail to set socket priority.\n");
    }

    // Set socket address
    struct sockaddr_in servaddr_a;
    memset(&servaddr_a, 0, sizeof(servaddr_a));
    servaddr_a.sin_family = AF_INET;
    servaddr_a.sin_addr.s_addr = inet_addr(VEHICLE_IP);
    servaddr_a.sin_port = htons(PORT_A);

    // Set socket address
    struct sockaddr_in servaddr_b;
    memset(&servaddr_b, 0, sizeof(servaddr_b));
    servaddr_b.sin_family = AF_INET;
    servaddr_b.sin_addr.s_addr = inet_addr(VEHICLE_IP);
    servaddr_b.sin_port = htons(PORT_B);

    std::cout << "Listening on port " << PORT_A << " and forwarding to port " << PORT_B << std::endl;
    std::cout << "Proxy running..." << std::endl;

    // Bind the second socket to a specific address
    if (bind(sockfd_b, (struct sockaddr *)&servaddr_b, sizeof(servaddr_b)) < 0) {
        std::cerr << "Error: Couldn't bind socket B." << std::endl;
        return -1;
    }

    if (listen(sockfd_b, 10) < 0) {
        std::cerr << "Error: Couldn't listen on socket B." << std::endl;
        return -1;
    }


    struct sockaddr_in ffmplay_addr;
    socklen_t ffmplay_len = sizeof(ffmplay_addr);

    // Connect to the client which executing "ffplay"
    int connfd_b = accept(sockfd_b, (struct sockaddr *)&ffmplay_addr, &ffmplay_len);
    if (connfd_b < 0) {
        std::cerr << "Error: Couldn't accept connection on socket B." << std::endl;
        return -1;
    }

    // Bind the first socket to a specific address
    if (bind(sockfd_a, (struct sockaddr *)&servaddr_a, sizeof(servaddr_a)) < 0) {
        std::cerr << "Error: Couldn't bind socket A." << std::endl;
        return -1;
    }

    if (listen(sockfd_a, 10) < 0) {
        std::cerr << "Error: Couldn't listen on socket A." << std::endl;
        return -1;
    }

    // Connect to the client which executing "ffmpeg"
    struct sockaddr_in client_addr;
    socklen_t client_len = sizeof(client_addr);
    int connfd_a = accept(sockfd_a, (struct sockaddr *)&client_addr, &client_len);
    if (connfd_a < 0) {
        std::cerr << "Error: Couldn't accept connection on socket A." << std::endl;
        return -1;
    }


    // Transfering
    char buffer[MAX_BUFFER_SIZE];
    ssize_t bytes_read;
    while ((bytes_read = read(connfd_a, buffer, MAX_BUFFER_SIZE)) > 0) {
	// Send streaming data from PORT_A to PORT_B
    ssize_t bytes_sent = 0;

        while(bytes_sent < bytes_read) {
            char *buf_ptr = buffer + bytes_sent;
            ssize_t sent = write(connfd_b, buf_ptr, bytes_read - bytes_sent);
            if (sent == 0) {
                std::cerr << "Error: Remote socket closed" << std::endl;
            } else if (sent < 0) {
                std::cerr << "Error: Couldn't write to socket B" << std::endl;
            } else {
                bytes_sent += sent;
            }
        }
    }
    if (bytes_read < 0) {
        std::cerr << "Error: Couldn't read from socket A." << std::endl;
        return -1;
    }

    // Close socket
    close(connfd_a);
    close(connfd_b);
    close(sockfd_a);
    close(sockfd_b);

    return 0;
}
