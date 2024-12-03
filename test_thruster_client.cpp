#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <cstring>

int main(){
    int client_socket;
    sockaddr_in server_addr;
    char buffer[1024] = {0};
    int addr_len = sizeof(server_addr);

    int port = 65432;

    if((client_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0){
        std::cerr << "Socket creation error" << std::endl;
        return -1;
    }
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    if(connect(client_socket, (struct sockaddr *)&server_addr, addr_len) < 0){
        std::cerr << "Connection failed" << std::endl;
        return -1;
    }

    recv(client_socket, buffer, 1024, 0);
    std::cout << buffer << std::endl;
    return 0;
}