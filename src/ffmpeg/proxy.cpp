#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>

#define MAX_BUFFER_SIZE 4096
#define PORT_A 8001 // 输入端口
#define PORT_B 8080 // 输出端口

const char* host = "140.112.31.243";

int main() {
    // 创建输入套接字
    int sockfd_a = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd_a < 0) {
        std::cerr << "Error: Couldn't create socket A." << std::endl;
        return -1;
    }

    // 创建输出套接字
    int sockfd_b = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd_b < 0) {
        std::cerr << "Error: Couldn't create socket B." << std::endl;
        return -1;
    }

    // Set socket priority
    int optval =  0;
    if(setsockopt(sockfd_b, SOL_SOCKET, SO_PRIORITY, &optval, sizeof(optval)) < 0){
        printf("Fail to set socket priority.\n");
    }

    // 设置输入套接字地址
    struct sockaddr_in servaddr_a;
    memset(&servaddr_a, 0, sizeof(servaddr_a));
    servaddr_a.sin_family = AF_INET;
    servaddr_a.sin_addr.s_addr = inet_addr(host);
    servaddr_a.sin_port = htons(PORT_A);

    // 设置输出套接字地址
    struct sockaddr_in servaddr_b;
    memset(&servaddr_b, 0, sizeof(servaddr_b));
    servaddr_b.sin_family = AF_INET;
    servaddr_b.sin_addr.s_addr = inet_addr(host);
    servaddr_b.sin_port = htons(PORT_B);

    std::cout << "Proxy running. Listening on port " << PORT_A << " and forwarding to port " << PORT_B << std::endl;

    // 绑定输入套接字到端口 B
    if (bind(sockfd_b, (struct sockaddr *)&servaddr_b, sizeof(servaddr_b)) < 0) {
        std::cerr << "Error: Couldn't bind socket B." << std::endl;
        return -1;
    }

    // 监听输入套接字
    if (listen(sockfd_b, 10) < 0) {
        std::cerr << "Error: Couldn't listen on socket B." << std::endl;
        return -1;
    }


    struct sockaddr_in ffmplay_addr;
    socklen_t ffmplay_len = sizeof(ffmplay_addr);

    int connfd_b = accept(sockfd_b, (struct sockaddr *)&ffmplay_addr, &ffmplay_len);
    if (connfd_b < 0) {
        std::cerr << "Error: Couldn't accept connection on socket B." << std::endl;
        return -1;
    }

    // 绑定输入套接字到端口 A
    if (bind(sockfd_a, (struct sockaddr *)&servaddr_a, sizeof(servaddr_a)) < 0) {
        std::cerr << "Error: Couldn't bind socket A." << std::endl;
        return -1;
    }

    // 监听输入套接字
    if (listen(sockfd_a, 10) < 0) {
        std::cerr << "Error: Couldn't listen on socket A." << std::endl;
        return -1;
    }

    // 接受连接
    struct sockaddr_in client_addr;
    socklen_t client_len = sizeof(client_addr);
    int connfd_a = accept(sockfd_a, (struct sockaddr *)&client_addr, &client_len);
    if (connfd_a < 0) {
        std::cerr << "Error: Couldn't accept connection on socket A." << std::endl;
        return -1;
    }


    // 开始转发数据
    char buffer[MAX_BUFFER_SIZE];
    ssize_t bytes_read;
    while ((bytes_read = read(connfd_a, buffer, MAX_BUFFER_SIZE)) > 0) {
	    // 发送数据到输出套接字
        if (write(connfd_b, buffer, bytes_read) != bytes_read) {
            std::cerr << "Error: Couldn't write to socket B." << std::endl;
            return -1;
        }
    }
    if (bytes_read < 0) {
        std::cerr << "Error: Couldn't read from socket A." << std::endl;
        return -1;
    }

    // 关闭套接字
    close(connfd_a);
    close(connfd_b);
    close(sockfd_a);
    close(sockfd_b);

    return 0;
}
