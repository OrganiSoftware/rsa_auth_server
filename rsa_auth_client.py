

import argparse
import os
import socket


class rsa_server_client:
    def rsa_server_client(self):
        parser = argparse.ArgumentParser(description='Create login login credetials for user rsa_auth')
        parser.add_argument('server_ip', help='ip for server connection')
        parser.add_argument('server_port', help='port for server connection')
        parser.add_argument('password', help='password for authentication')
        args = parser.parse_args()
        host = socket.gethostname()
        username = str(socket.gethostbyname(host)) + '-' + str(args.server_ip)
        print(str(username))
        os.system("echo "+str(username))
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((args.server_ip, int(args.server_port)))
        message = "get_client_public_key:" + str(username)
        client_socket.send(message.encode())
        public_key = client_socket.recv(8192).decode()
        print(str(public_key))
        with open("/home/organi/client_pubkey.txt,asc", "w") as file:
            file.write(str(public_key))
            file.close()
        os.system("echo "+str(args.password)+" > ~/pass.txt")
        os.system("gpg --import ~/client_pubkey.txt,asc")
        os.system("gpg -a -e  -r "+str(username)+" ~/pass.txt")
        os.system("echo "+str(username)+" > ~/user.txt")
        os.system("gpg -a -e -r "+str(username)+" ~/user.txt")
        os.system("rm ~/pass.txt; rm ~/user.txt")
        os.system("cat ~/user.txt.asc > ~/userasc.txt ")
        os.system("cat ~/pass.txt.asc > ~/passasc.txt")
        rsa_auth = ""
        with open("/home/organi/userasc.txt", "r") as file:
            print(file.read())
            rsa_auth = file.read() + ':'
            file.close()
        with open("/home/organi/passasc.txt", "r") as file:
            print(str(file.read()))
            rsa_auth = rsa_auth + file.read()
            file.close()

        with open("/home/organi/rsa_auth.txt" , "w") as file:
            user = open("/home/organi/userasc.txt", "r")
            password = open("/home/organi/passasc.txt", "r")
            file.write("auth_user:")
            file.write(str(user.read()))
            file.write(":")
            file.write(str(password.read()))
            file.close()
        rsa_auth = open("/home/organi/rsa_auth.txt" , "r")
        print(str(rsa_auth.read()))
        message = rsa_auth.read()
        output = None
        while output != "fail" and output != 'exit':
            client_socket.send(message.encode())
            output = client_socket.recv(8192).decode()
            message = input(" -> ")

        client_socket.close()

if __name__ == '__main__':
    rsa_server_client = rsa_server_client()
    rsa_server_client.rsa_server_client()
