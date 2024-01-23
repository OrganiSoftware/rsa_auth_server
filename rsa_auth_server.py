import os
import socket

class rsa_server:
    def rsa_server(self):
        host = socket.gethostname()
        host_ip = socket.gethostbyname(host)
        port = 3000
        print(host)
        print(host_ip)
        os.system("echo " + str(host) + "")
        os.system("echo " + str(host_ip) + "")
        server_socket = socket.socket()
        server_socket.bind((host_ip, port))
        server_socket.listen(2)
        conn, addr = server_socket.accept()
        is_data_stream = True
        while is_data_stream:
            data = conn.recv(1024).decode()
            if not data:
            # if data is not received break
                break
            data = data.split(':')
            username = None
            print(data)
            if data[0] == "get_client_public_key":
                os.system("gpg --export -a " + str(data[1])+"> ~/pubkey.txt.asc")
                username = str(data[1])
                data = open("/home/organi/pubkey.txt.asc", "r")
                data = data.read()
                print(data)
                conn.send(data.encode())

            data = conn.recv(8192).decode()
            data = data.split(':')
            print(data)
            if data[0] == "auth_user":
                with open("/home/organi/asci_usrname.txt.asc", "w") as file:
                    print(str(data[1]))
                    file.write(str(data[1]))
                    file.close()
                with open("/home/organi/asci_password.txt.asc", "w") as file:
                    print(str(data[2]))
                    file.write(str(data[2]))
                    file.close()
                os.system("gpg -d -a -u "+ str(username)+"  ~/asci_usrname.txt.asc >~/asci_username.txt.out")
                os.system("gpg -d -a -u " + str(username) + "  ~/asci_password.txt.asc >~/asci_password.txt.out")
                os.system("gpg -d  -a -u "+username+" ~/"+username+"_password_file.txt.asc > ~/"+username+"_password_file.txt.out")
                password = open("/home/organi/asci_password.txt.out")
                server_side_pass = open("/home/organi/"+username+"_password_file.txt.out")
                if password != server_side_pass.read():
                    data = "fail"
                    is_data_stream = False
                    conn.send(data.encode())
            if data == "exit":
                is_data_stream = False
                conn.send(data.encode())
            data = input(' -> ')
            conn.send(data.encode())

        conn.close()  # close the connection


if __name__ == '__main__':
    rsa_server = rsa_server()
    rsa_server.rsa_server()
