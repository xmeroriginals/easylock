import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Security and format constants
SALT_SIZE = 16
NONCE_SIZE = 12
ITERATIONS = 200_000
EXTENSION = ".elock"

class CryptoError(Exception):
    """Base exception for all cryptographic operations in EasyLock."""
    pass

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a cryptographically strong 32-byte key using PBKDF2-HMAC-SHA256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))

def encrypt_file(file_path: str, password: str, keep_original: bool = False) -> str:
    """
    Encrypt a file using AES-256-GCM.
    
    Data format: [SALT (16 bytes)][NONCE (12 bytes)][CIPHERTEXT + AUTH TAG]
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found: {file_path}")
    
    if file_path.endswith(EXTENSION):
        raise CryptoError("File is already encrypted.")

    try:
        salt = os.urandom(SALT_SIZE)
        key = derive_key(password, salt)
        aesgcm = AESGCM(key)
        nonce = os.urandom(NONCE_SIZE)

        with open(file_path, 'rb') as f:
            data = f.read()

        ciphertext = aesgcm.encrypt(nonce, data, None)
        output_path = file_path + EXTENSION
        
        with open(output_path, 'wb') as f:
            f.write(salt)
            f.write(nonce)
            f.write(ciphertext)
            
        if not keep_original:
            os.remove(file_path)
            
        return output_path
    except Exception as e:
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)
        raise e

def decrypt_file(file_path: str, password: str, keep_original: bool = False) -> str:
    """
    Decrypt a .elock file and restore the original content.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Encrypted file not found: {file_path}")
    
    if not file_path.endswith(EXTENSION):
        raise CryptoError("File format not supported (missing .elock extension).")

    try:
        with open(file_path, 'rb') as f:
            salt = f.read(SALT_SIZE)
            nonce = f.read(NONCE_SIZE)
            ciphertext = f.read()
            
        if len(salt) != SALT_SIZE or len(nonce) != NONCE_SIZE:
            raise CryptoError("File structure is corrupted or invalid.")

        key = derive_key(password, salt)
        aesgcm = AESGCM(key)
        
        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        except Exception:
            raise CryptoError("Invalid password or corrupted file.")
            
        output_path = file_path[:-len(EXTENSION)]
        
        # Prevent collision with an existing file by appending a suffix
        if os.path.exists(output_path):
            base, ext = os.path.splitext(output_path)
            output_path = f"{base}_decrypted{ext}"
            
        with open(output_path, 'wb') as f:
            f.write(plaintext)
            
        if not keep_original:
            os.remove(file_path)
            
        return output_path
    except Exception as e:
        raise e
