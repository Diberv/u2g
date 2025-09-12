import json
import os
import socket
import threading
import math
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

version = "0.1"

#settings
script_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(script_dir, "settings.json")
with open(settings_path, "r", encoding="utf-8") as file:
    data = json.load(file)
    debug_message = data.get("debug").get("message")
    client_queue_size = data.get("client_queue_size")
    server_port = data.get("server_port")
    timeout_seconds = data.get("timeout_seconds")
    CHUNK_SIZE = data.get("chunk_size_bytes")

    #RSA keys


    private_key = data.get("keys").get("private_key").encode()
    public_key = data.get("keys").get("public_key").encode()


    #file size limit

    if data.get("max_file_size_mb").get("gigabytes") != 0:
        fileSize = data.get("max_file_size_mb").get("gigabytes") * 1024 * 1024 * 1024
    elif data.get("max_file_size_mb").get("megabytes") != 0:
        fileSize = data.get("max_file_size_mb").get("megabytes") * 1024 * 1024
    elif data.get("max_file_size_mb").get("kilobytes") != 0:
        fileSize = data.get("max_file_size_mb").get("kilobytes") * 1024
    elif data.get("max_file_size_mb").get("bytes") != 0:
        fileSize = data.get("max_file_size_mb").get("bytes")
    else:
        print("No valid file size specified in settings.json. Please specify gigabytes, megabytes, kilobytes, or bytes.")
        exit()
    print (f"Max file size set to {fileSize} bytes")


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
    private_key = serialization.load_pem_private_key(
        private_key,
        password=None,
        backend=default_backend()
    )
    original_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_message



p2p_clients = {}


def write_to_server(public_key, conn, data):
    print("ok")








#methods




def p2p(conn, addr, client_public_key):
    data = conn.recv(1024)
    print(RSA_decrypt(private_key, data).decode())



































def handle_client(conn, addr):
    print('connected:', addr) if debug_message else None
    try:
        conn.settimeout(2)

        # Handshake
        data = conn.recv(1024)
        conn.send(version.encode())

        try:
            data = data.decode()
            print(f"Client version: {data} {addr}") if debug_message else None
            if data != version:
                print(f"Client version mismatch {addr}") if debug_message else None
                conn.close()
                exit()
            else:
                #metod
                data = conn.recv(1024)
                if data.decode() == "p2p":
                    conn.send(public_key)
                    client_public_key = conn.recv(1024).decode()
                    conn.settimeout(None)
                    threading.Thread(target=p2p, args=(conn, addr, client_public_key), daemon=True).start()


                    
        except UnicodeError:
            print(f"Received invalid data {addr}") if debug_message else None
            conn.close()
            exit()

    except TimeoutError:
        print(f"Data receive timeout exceeded {addr}") if debug_message else None
        conn.close()



sock = socket.socket()
sock.bind(('', 9090))
sock.listen(client_queue_size)

while True:
    conn, addr = sock.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()