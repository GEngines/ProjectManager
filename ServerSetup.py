






import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432       # Port to listen on (non-privileged ports are > 1023)


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             data = data.decode()
#             print("DataType : ", type(data))
#             print("Decode Eval : " , type(eval(data)))
#             print("Data received : ", data)
#             if not data:
#                 break

_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_socket.bind((HOST, PORT))

close_connection = False
while not close_connection:
    print("Listening...")
    _socket.listen()
    conn, addr = _socket.accept()
    print("Connected!", addr)
    keep_alive = True

    while keep_alive:
        data = conn.recv(1024)
        data = data.decode()
        try:
            data = eval(data)
        except:
            data = data
        print("Data received : ", data)
        print("Data Type : ", type(data))

        if data == "close link":
            print("Closing Connection.")
            keep_alive = False

        if data == "close server":
            print("Stopping Server.")
            keep_alive = False
            close_connection = True












