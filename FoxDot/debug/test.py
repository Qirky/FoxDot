import socket

sock = socket.socket()
sock.bind(('localhost',57110))

while True:
    sock.listen(1)
    

