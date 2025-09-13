import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import random
import string




def random_string(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for i in range(length))



my_name = random_string(12)
print(f"my_name: {my_name}")

text = str(input())

version = "0.1"


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



def start():
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
        sock.send("p2p".encode())

        server_public_key = sock.recv(2048)
        sock.send(pem_public_key)
        
        #sock.send(RSA_encrypt(server_public_key, text.encode()))

        #p2p
        sock.send(RSA_encrypt(server_public_key, my_name.encode()))

        print(RSA_decrypt(private_key, sock.recv(256)).decode())


        
start()