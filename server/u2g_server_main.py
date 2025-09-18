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
waiting_clients = []  # client_id
connected_pairs = {}  # client_id -> peer_client_id
thread_events = {}


def write_to_client_RSA(public_key, conn, data):
    try:
        try:
            
            text = RSA_encrypt(public_key, data.encode())
        
            conn.send(text)
        except (BrokenPipeError, ConnectionResetError) as e:
            print(f"disconnected, Exeption: {e}") if debug_message else None
            return None

    except Exception as e:
        print(f"exeption_write: {e}") if debug_message else None


def read_to_client_RSA(private_key, conn):
    try:
        data = conn.recv(256)
        if not data:
            print('disconnected') if debug_message else None
            return None
        text = RSA_decrypt(private_key, data)
        return text.decode()
    except Exception as e:
        print(f"exeption_read: {e}") if debug_message else None






#methods




def p2p(conn, addr, client_public_key):
    try:
        client_id = read_to_client_RSA(private_key, conn)
        if client_id in p2p_clients:
            conn.close()
        else:
            p2p_clients[client_id] = conn
            #print(p2p_clients)
            write_to_client_RSA(client_public_key, conn, "ok")
            data = read_to_client_RSA(private_key, conn)

            if data == "create":
                waiting_clients.append(client_id)
                thread_events[client_id] = threading.Event()
                thread_events[client_id].wait()
                peer_client_id = connected_pairs[client_id]

                while True:
                    data = conn.recv(4096)
                    p2p_clients[peer_client_id].send(data)

            if data == "join":
                peer_client_id = read_to_client_RSA(private_key, conn)
                if peer_client_id in waiting_clients:
                    connected_pairs[client_id] = peer_client_id
                    connected_pairs[peer_client_id] = client_id
                    waiting_clients.remove(peer_client_id)
                    thread_events[peer_client_id].set()

                    while True:
                        data = conn.recv(4096)
                        p2p_clients[peer_client_id].send(data)


                else:
                    conn.close()


    except Exception as e:
        print(f"exeption_read: {e}") if debug_message else None
        






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
                    client_public_key = conn.recv(2048)
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