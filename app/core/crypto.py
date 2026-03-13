import os
import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, hmac
from argon2.low_level import hash_secret_raw, Type

MAGIC_HEADER = b"ELCK"
VERSION = b"\x02\x00"
SALT_SIZE = 16
NONCE_SIZE = 16
CHUNK_SIZE = 64 * 1024
EXTENSION = ".elock"
LEGACY_NONCE_SIZE = 12
ARGON2_TIME_COST = 2
ARGON2_MEMORY_COST = 102400
ARGON2_PARALLELISM = 4

class CryptoError(Exception):
    pass

def derive_keys(password: str, salt: bytes, time_cost: int, memory_cost: int, parallelism: int) -> tuple[bytes, bytes]:
    key_material = hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism=parallelism,
        hash_len=64,
        type=Type.ID
    )
    return key_material[:32], key_material[32:]

def secure_delete(file_path: str):
    if not os.path.exists(file_path):
        return
    try:
        file_size = os.path.getsize(file_path)
        with open(file_path, 'r+b') as f:
            f.seek(0)
            written = 0
            while written < file_size:
                write_size = min(CHUNK_SIZE, file_size - written)
                f.write(os.urandom(write_size))
                written += write_size
            f.flush()
            os.fsync(f.fileno())
    except Exception:
        pass
    finally:
        try:
            os.remove(file_path)
        except Exception:
            pass

def encrypt_file(file_path: str, password: str, keep_original: bool = False) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found: {file_path}")
    
    if file_path.endswith(EXTENSION):
        raise CryptoError("File is already encrypted.")

    try:
        salt = os.urandom(SALT_SIZE)
        encryption_key, mac_key = derive_keys(
            password, salt, ARGON2_TIME_COST, ARGON2_MEMORY_COST, ARGON2_PARALLELISM
        )
        nonce = os.urandom(NONCE_SIZE)
        cipher = Cipher(algorithms.AES(encryption_key), modes.CTR(nonce))
        encryptor = cipher.encryptor()
        params_bytes = struct.pack('<III', ARGON2_TIME_COST, ARGON2_MEMORY_COST, ARGON2_PARALLELISM)
        mac = hmac.HMAC(mac_key, hashes.SHA256())
        mac.update(MAGIC_HEADER)
        mac.update(VERSION)
        mac.update(params_bytes)
        mac.update(salt)
        mac.update(nonce)
        output_path = file_path + EXTENSION
        temp_output_path = output_path + ".tmp"
        
        with open(file_path, 'rb') as f_in, open(temp_output_path, 'wb') as f_out:
            f_out.write(MAGIC_HEADER)
            f_out.write(VERSION)
            f_out.write(params_bytes)
            f_out.write(salt)
            f_out.write(nonce)
            
            while True:
                chunk = f_in.read(CHUNK_SIZE)
                if not chunk:
                    break
                ciphertext_chunk = encryptor.update(chunk)
                f_out.write(ciphertext_chunk)
                mac.update(ciphertext_chunk)
                
            ciphertext_chunk = encryptor.finalize()
            if ciphertext_chunk:
                f_out.write(ciphertext_chunk)
                mac.update(ciphertext_chunk)
                
            f_out.write(mac.finalize())
            
        os.replace(temp_output_path, output_path)
            
        if not keep_original:
            secure_delete(file_path)
            
        return output_path
    except Exception as e:
        if 'temp_output_path' in locals() and os.path.exists(temp_output_path):
            secure_delete(temp_output_path)
        if 'output_path' in locals() and os.path.exists(output_path):
            secure_delete(output_path)
        raise e

def decrypt_file(file_path: str, password: str, keep_original: bool = False) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Encrypted file not found: {file_path}")
    
    if not file_path.endswith(EXTENSION):
        raise CryptoError("File format not supported (missing .elock extension).")

    try:
        with open(file_path, 'rb') as f:
            header_probe = f.read(len(MAGIC_HEADER))
            is_legacy = (header_probe != MAGIC_HEADER)
            
            if not is_legacy:
                version = f.read(len(VERSION))
                if len(version) < len(VERSION):
                    raise CryptoError("Bozuk dosya başlığı (Sürüm bilgisi eksik).")

                if version == b"\x01\x00":
                    t_cost, m_cost, p_factor = 2, 102400, 4
                    params_bytes = b""
                elif version == b"\x02\x00":
                    params_bytes = f.read(12)
                    if len(params_bytes) < 12:
                        raise CryptoError("Bozuk dosya başlığı (Parametre verisi eksik).")
                    t_cost, m_cost, p_factor = struct.unpack('<III', params_bytes)
        
                    if m_cost > 1024 * 1024:
                        raise CryptoError("Geçersiz veya çok yüksek bellek maliyeti (>1GB). DoS koruması.")
                    if t_cost > 100:
                        raise CryptoError("Geçersiz veya çok yüksek zaman maliyeti (iterasyon).")
                    if p_factor > 64:
                        raise CryptoError("Geçersiz veya çok yüksek paralellik değeri.")
                        
                else:
                    raise CryptoError("Unsupported encryption version.")
                
                salt = f.read(SALT_SIZE)
                if len(salt) < SALT_SIZE:
                    raise CryptoError("Bozuk dosya başlığı (Salt eksik).")
                nonce = f.read(NONCE_SIZE)
                if len(nonce) < NONCE_SIZE:
                    raise CryptoError("Bozuk dosya başlığı (Nonce eksik).")
            else:
                f.seek(0)
                salt = f.read(SALT_SIZE)
                nonce = f.read(LEGACY_NONCE_SIZE)
                
        output_path = file_path[:-len(EXTENSION)]
        if os.path.exists(output_path):
            base, ext = os.path.splitext(output_path)
            output_path = f"{base}_decrypted{ext}"
            
        temp_output_path = output_path + ".tmp"
        
        if is_legacy:
            file_size = os.path.getsize(file_path)
            data_size = file_size - SALT_SIZE - LEGACY_NONCE_SIZE - 16
            if data_size < 0:
                raise CryptoError("File structure is corrupted or invalid.")
                
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=200_000,
            )
            key = kdf.derive(password.encode("utf-8"))
            
            try:
                with open(file_path, 'rb') as f_leg, open(temp_output_path, 'wb') as f_out:
                    f_leg.seek(file_size - 16)
                    tag = f_leg.read(16)
                    
                    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
                    decryptor = cipher.decryptor()
                    
                    f_leg.seek(SALT_SIZE + LEGACY_NONCE_SIZE)
                    data_read = 0
                    while data_read < data_size:
                        read_size = min(CHUNK_SIZE, data_size - data_read)
                        chunk = f_leg.read(read_size)
                        if not chunk: break
                        
                        plaintext_chunk = decryptor.update(chunk)
                        f_out.write(plaintext_chunk)
                        data_read += len(chunk)
                        
                    plaintext_chunk = decryptor.finalize()
                    if plaintext_chunk:
                        f_out.write(plaintext_chunk)
            except Exception:
                if os.path.exists(temp_output_path):
                    secure_delete(temp_output_path)
                raise CryptoError("Invalid password or corrupted file.")
                
            os.replace(temp_output_path, output_path)
            
        else:
            mac_size = 32
            file_size = os.path.getsize(file_path)
            header_overhead = len(MAGIC_HEADER) + len(VERSION) + len(params_bytes) + SALT_SIZE + NONCE_SIZE
            data_size = file_size - header_overhead - mac_size
            if data_size < 0:
                raise CryptoError("File structure is corrupted or invalid.")
                
            encryption_key, mac_key = derive_keys(password, salt, t_cost, m_cost, p_factor)
            mac = hmac.HMAC(mac_key, hashes.SHA256())
            mac.update(MAGIC_HEADER)
            mac.update(VERSION)
            if version == b"\x02\x00":
                mac.update(params_bytes)
            mac.update(salt)
            mac.update(nonce)
            
            cipher = Cipher(algorithms.AES(encryption_key), modes.CTR(nonce))
            decryptor = cipher.decryptor()
            
            try:
                with open(file_path, 'rb') as f_in, open(temp_output_path, 'wb') as f_out:
                    f_in.seek(header_overhead)
                    
                    data_read = 0
                    while data_read < data_size:
                        read_size = min(CHUNK_SIZE, data_size - data_read)
                        chunk = f_in.read(read_size)
                        if not chunk: break
                        
                        mac.update(chunk)
                        plaintext_chunk = decryptor.update(chunk)
                        f_out.write(plaintext_chunk)
                        data_read += len(chunk)
                        
                    plaintext_chunk = decryptor.finalize()
                    if plaintext_chunk:
                        f_out.write(plaintext_chunk)
                        
                    stored_mac = f_in.read(mac_size)
                    if len(stored_mac) < mac_size:
                        raise CryptoError("Bozuk dosya (MAC imzası eksik veya dosya kesilmiş).")
                    mac.verify(stored_mac)
            except Exception:
                if os.path.exists(temp_output_path):
                    secure_delete(temp_output_path)
                raise CryptoError("Invalid password or corrupted file.")
                
            os.replace(temp_output_path, output_path)
            
        if not keep_original:
            secure_delete(file_path)
            
        return output_path
    except Exception as e:
        raise e
