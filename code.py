
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

# AES Encryption
class AESEncryption:
    def __init__(self, key: bytes):
        self.key = key

    def encrypt(self, plaintext: str) -> tuple:
        iv = os.urandom(16)  # Generate a random IV
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_plaintext = plaintext.ljust(32)  # Padding for block size
        ciphertext = encryptor.update(padded_plaintext.encode()) + encryptor.finalize()
        return iv, ciphertext

    def decrypt(self, iv: bytes, ciphertext: bytes) -> str:
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_text.strip().decode()

# Generate a random key for AES
key = os.urandom(32)
aes = AESEncryption(key)
iv, encrypted_text = aes.encrypt("Smart Grid Secure Data")
print("Encrypted:", encrypted_text)
print("Decrypted:", aes.decrypt(iv, encrypted_text))

# ECC Encryption (Elliptic Curve Cryptography)
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def generate_ecc_keys():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

def sign_data(private_key, data: str):
    signature = private_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))
    return signature

def verify_signature(public_key, data: str, signature: bytes):
    try:
        public_key.verify(signature, data.encode(), ec.ECDSA(hashes.SHA256()))
        return True
    except Exception:
        return False

private_key, public_key = generate_ecc_keys()
data = "Secure Smart Grid Communication"
signature = sign_data(private_key, data)
print("ECC Signature Verified:", verify_signature(public_key, data, signature))

# AI-Driven Threat Detection using ML
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomalies(data_samples):
    model = IsolationForest(contamination=0.1)
    model.fit(data_samples)
    anomalies = model.predict(data_samples)
    return anomalies

# Simulated smart grid data
power_data = np.random.normal(loc=50, scale=5, size=(100, 1))  # Normal readings
power_data = np.vstack((power_data, [[100], [110], [120]]))  # Injecting anomalies
anomalies_detected = detect_anomalies(power_data)
print("Anomalies:", anomalies_detected[-5:])
