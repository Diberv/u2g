import json
import os
import socket
import threading
import math

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

client_id_to_take = []
client_to_write = []

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
                data = conn.recv(1024)
                #client_id_to_take.append(conn)
                if data.decode() == "write":
                    try:
                        conn.send(str(fileSize).encode())
                        data = conn.recv(1024).decode()

                        if int(data) <= fileSize:
                            with open(os.path.join(script_dir, str(addr)), "w", encoding="utf-8") as f:
                                data = conn.recv(fileSize)
                                f.write(data.decode())
                                client_to_write.append(str(addr))


                    finally:
                        #client_id_to_take.remove(conn)
                        print(f"Client disconnected {addr}") if debug_message else None
                        conn.close()
                    
        except UnicodeError:
            print(f"Received invalid data {addr}") if debug_message else None
            conn.close()
            exit()

    except TimeoutError:
        print(f"Data receive timeout exceeded {addr}") if debug_message else None
        conn.close()


    conn.close()

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(client_queue_size)

while True:
    conn, addr = sock.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()