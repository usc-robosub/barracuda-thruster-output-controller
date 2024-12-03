#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
// for linux
// #include <netinet/in.h>
// #include <sys/socket.h>
// #include <unistd.h>

#include <fstream>
#include <nlohmann/json.hpp> // json library

using json = nlohmann::json;



int main(){
    int server_socket, client_socket; // file descriptor for socket
    sockaddr_in server_addr;
    char buffer[1024] = {0};
    int addr_len = sizeof(server_addr);

    int port = 65432;//port number

    std::ifstream infile("thruster_pwm.json");
    json thruster_pwm_json = json::parse(infile); // parse thruster pwm values from thruster_pwm.json
    infile.close(); 


    if((server_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0){
        std::cerr << "Socket creation error" << std::endl;
        return -1;
    }
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    if(bind(server_socket, (struct sockaddr *)&server_addr, addr_len) < 0){
        std::cerr << "bind failed" << std::endl;
        return -1;
    }

    if(listen(server_socket, 5) < 0){
        std::cerr << "listen failed" << std::endl;
        return -1;
    }

    clinet_socket = accept(server_socket, (struct sockaddr *)&server_addr, (socklen_t*)&addr_len);

    if(client_socket < 0){
        std::cerr << "accept failed" << std::endl;
        return -1;
    }
    const char msg[] = thruster_pwm_json.dump().c_str();

    send(client_socket, msg, strlen(msg), 0);
    std::cout << msg <<"\n json message sent" << std::endl;
    
}