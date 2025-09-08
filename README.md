# u2g
U2G (User-to-Global) is a Python library for secure messaging through public servers. Each message is encrypted on the sender’s side and can be sent to a server that broadcasts it to all connected users. Thanks to encryption, only the recipient can read the message content, ensuring privacy even over public channels.

---

## 📌 Description

- The server acts as an intermediary for message delivery.  
- Each client has its own key pair (public and private).  
- When sending data, the server retrieves the public keys of all connected clients.  
- The sender selects the target recipient, encrypts the message with their public key, and sends the packet to the server.  
- The server distributes the packet to all clients, but only the intended recipient can decrypt it.

---

## ⚠️ Important

Before running, you must install dependencies and set up the environment.  
u2g will not work otherwise.
