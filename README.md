# u2g
U2G (User-to-Global) is a Python library for secure messaging through public servers. Each message is encrypted on the sender’s side and can be sent to a server that broadcasts it to all connected users. Thanks to encryption, only the recipient can read the message content, ensuring privacy even over public channels.

---

## 📌 Description

- The server acts as an intermediary for message delivery.  
- Each client has its own key pair (public and private).   
- The sender selects the target recipient, encrypts the message with their public key, and sends the packet to the server.  
- The server distributes the packet to all clients, but only the intended recipient can decrypt it.

## 🔐 Encryption

u2g uses public-key cryptography to ensure that only the intended recipient can decrypt the data.  
The main steps of the encryption process are:

1. **Key pairs**  
   - Each client has a public and private key.  
   - Public keys are shared with the server; private keys remain confidential on the client side.

2. **Encrypting messages**  
   - When sending data, the sender retrieves the recipient's public key from the server.  
   - The message or session key is encrypted with the recipient's public key.  

3. **Server relay**  
   - The encrypted packet is sent to the server, which distributes it to all connected clients.  
   - Only the client with the corresponding private key can decrypt the message.

4. **Supported algorithms**  
   - Currently, SHA-256 and SHA-512 are used for hashing and verification.  
   - Future updates may add additional encryption standards.

This system ensures secure communication between clients, even when the server relays the data.

---

## ⚠️ Important

Before running, you must install dependencies and set up the environment.  
u2g will not work otherwise.
