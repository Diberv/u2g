import socket

textre = str(input())

version = "0.1"


sock = socket.socket()
sock.connect(('localhost', 9090))
# Handshake
sock.send(version.encode())
data = sock.recv(1024)
if data.decode() != version:
    print("Version mismatch")
    sock.close()
    exit()
else:
    sock.send("write".encode())
    maxsize = str(sock.recv(1024).decode())
    
    if len(textre) <= int(maxsize):
        sock.send(str(len(textre)).encode())
        sock.send(textre.encode())
        print("Data sent")
    else:
        print("Data too large max is " + maxsize)


sock.close()

print(data)