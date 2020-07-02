


import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


data_to_send = [1, 2, 3, 4, 5]
print("DataType : ", type(data_to_send))
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(str(data_to_send).encode())
#     data = s.recv(1024)
#     print("Data Sent!")
#
# # print('Received', repr(data))

_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_socket.connect((HOST, PORT))

keep_alive = True

while keep_alive:
    user_input = eval(input("Enter your Information : "))
    print ("Data Type : ", type(user_input))
    data = str(user_input).encode()
    _socket.sendall(data)
    if user_input == "close link" or user_input == "close server":
        keep_alive = False


