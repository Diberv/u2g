import socket
import threading
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import random
import json
import string

method = None

script_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(script_dir, "settings.json")
def setmethod(met):
    with open(settings_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    data['method'] = met
    with open(settings_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    with open(settings_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        global method
        method = data.get("method")

setmethod("None")




def random_string(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for i in range(length))



my_name = random_string(12)
print(f"my_name: {my_name}")

#text = str(input())

version = "0.1"
p2p_mode = ""

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)


public_key = private_key.public_key()

pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

pem_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)





def RSA_encrypt(public_key, message):
    public_key = serialization.load_pem_public_key(
        public_key,
        backend=default_backend()
    )
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def RSA_decrypt(private_key, encrypted_message):
    original_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_message




def write_to_client_RSA(public_key, conn, data):
    try:
        try:
            
            text = RSA_encrypt(public_key, data.encode())
        
            conn.send(text)
        except (BrokenPipeError, ConnectionResetError) as e:
            print(f"disconnected, Exeption: {e}")
            return None

    except Exception as e:
        print(f"exeption_write: {e}")


def read_to_client_RSA(private_key, conn):
    try:
        data = conn.recv(256)
        if not data:
            print('disconnected')
            return None
        text = RSA_decrypt(private_key, data)
        return text.decode()
    except Exception as e:
        print(f"exeption_read: {e}")



def p2p_read(sock):
    while True:
        print(sock.recv(4096).decode())

def p2p(mode, sock, server_public_key):
    if mode == "create":
        threading.Thread(target=p2p_read, daemon=True, args=(sock,)).start()
        threading.Thread(target=p2p_write, args=(sock, client_public_key), daemon=True).start()

    if mode == "join":
        write_to_client_RSA(server_public_key, sock, input("id: "))
        threading.Thread(target=p2p_read, daemon=True, args=(sock,)).start()
        while True:
            sock.send(input().encode())




join = ""


def start(ip, port):
    sock = socket.socket()
    sock.connect((ip, port))
    # Handshake
    sock.send(version.encode())
    data = sock.recv(1024)
    if data.decode() != version:
        print("Version mismatch")
        sock.close()
        exit()
    else:
        sock.send("p2p".encode())

        server_public_key = sock.recv(2048)
        sock.send(pem_public_key)
        
        #sock.send(RSA_encrypt(server_public_key, text.encode()))

        #p2p  
        write_to_client_RSA(server_public_key, sock, my_name)
        read_to_client_RSA(private_key, sock)

        if method == "p2p":
            if p2p_mode != "":
                if join != "":
                    write_to_client_RSA(server_public_key, sock, p2p_mode)
                    p2p(p2p_mode, sock, server_public_key)
                else:
                    raise ValueError("you didn't select a join code")
            else:
                raise ValueError("you didn't select a mode")
            

setmethod("p2p")
p2p_mode = input("join/create: ")        
start("localhost", 9090)
