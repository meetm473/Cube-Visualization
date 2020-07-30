import socket

LISTENING_PORT = 1620
buff = 1024

# Creating an INET(IPv4) and STREAMing socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""
Creation of a server socket and binding to a host address
which listens to a port. The socket is reachable by any address the
machine has due to specifying '' in the place of host IP address
"""
serverSocket.bind(('', LISTENING_PORT))

# becoming a server and letting at max 1 client to join
serverSocket.listen(1)

while True:
    # accept connection from outside
    conn,addr = serverSocket.accept()
    data = conn.recv(buff)
    print("received data: ", data)
print("done!")
conn.close()
