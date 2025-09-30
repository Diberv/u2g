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

---

## 🚀 Features
- 🔐 RSA key generation (2048-bit) for client and server.  
- 📩 Encryption and decryption of messages using `OAEP + SHA256`.  
- 🔗 Establishing a secure P2P connection over TCP socket.  
- ⚡ Two modes of operation:
  - `create` — create a session.  
  - `join` — connect to an existing session.  
- 🛠 Configuration through the `settings.json` file.  
- 📜 Automatic generation of a unique name for each client.  

---

## 📂 Project Structure
```
.
├── u2g.py          # Main client: connection, encryption, P2P logic
├── get_keys.py     # Utility for generating new RSA keys
├── settings.json   # Configuration file (automatically updated by the script)
└── README.md       # Documentation
```

---

## ⚙️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/username/repo.git
   cd repo
   ```

2. Install dependencies:
   ```bash
   pip install cryptography
   ```

3. Make sure Python 3.8+ is installed:
   ```bash
   python --version
   ```

---

## ▶️ Usage

### 🔑 Generating keys
```bash
python get_keys.py
```
The script will print the private and public keys in PEM format.

---

### 📡 Running the client
```bash
python u2g.py
```

Then choose the mode:
- `create` — creates a new P2P session.  
- `join` — connects to an existing session.  

Example:
```
join/create: create
```

---

## 🧩 Key Functions

### 🔑 Encryption and Decryption
- `RSA_encrypt(public_key, message)` — encrypt a message.  
- `RSA_decrypt(private_key, encrypted_message)` — decrypt a message.  

### 🔗 Server Interaction
- `start(ip, port)` — connects the client to the server, exchanges versions and keys.  
- `p2p(mode, sock, server_public_key)` — runs the P2P mode (create/join).  

### ⚙️ Utilities
- `setmethod(met)` — updates the `method` field in `settings.json`.  
- `random_string(length)` — generates a random client name.  

---

## 📖 Example Workflow
1. First client runs:
   ```
   join/create: create
   ```
   → A session is created, incoming messages are displayed.

2. Second client runs:
   ```
   join/create: join
   id: <ID of the first client>
   ```
   → A connection is established, communication happens through encrypted messages.

---

## 🔐 Security
- Uses asymmetric RSA-2048 encryption.  
- Messages are encrypted with `OAEP + SHA256`.  
- The private key is **never transmitted** over the network.  
- Can be extended to a hybrid scheme (RSA + AES).  

---

## 🛠 Roadmap
- [ ] Add support for symmetric encryption (AES) after RSA key exchange.  
- [ ] Move the server to a separate module.  
- [ ] Add tests (`pytest`).  
- [ ] Add GUI or web interface support.  

---

## 📜 License
MIT License. Free to use and modify.
