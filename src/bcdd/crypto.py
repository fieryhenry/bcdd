import enum
import hashlib
import random
from typing import Optional
from Cryptodome.Cipher import AES
from bcdd import data


class HashAlgorithm(enum.Enum):
    MD5 = enum.auto()
    SHA1 = enum.auto()
    SHA256 = enum.auto()


class Hash:
    def __init__(self, algorithm: HashAlgorithm, data: "data.Data"):
        self.algorithm = algorithm
        self.data = data

    def get_hash(self, length: Optional[int] = None) -> "data.Data":
        if self.algorithm == HashAlgorithm.MD5:
            hash = hashlib.md5()
        elif self.algorithm == HashAlgorithm.SHA1:
            hash = hashlib.sha1()
        elif self.algorithm == HashAlgorithm.SHA256:
            hash = hashlib.sha256()
        else:
            raise ValueError("Invalid hash algorithm")
        hash.update(self.data.get_bytes())
        if length is None:
            return data.Data(hash.digest())
        return data.Data(hash.digest()[:length])

    @staticmethod
    def get_decryption_key() -> str:
        return Hash(HashAlgorithm.MD5, data.Data("battlecats")).get_hash(8).to_hex()


class AesCipher:
    def __init__(
        self,
        key: bytes,
        iv: Optional[bytes] = None,
        mode: Optional[int] = None,
        enable: bool = True,
    ):
        self.key = key
        self.iv = iv
        if mode is None:
            if iv is None:
                mode = AES.MODE_ECB
            else:
                mode = AES.MODE_CBC
        self.mode = mode
        self.enable = enable

    def get_cipher(self):
        if self.iv is None:
            return AES.new(self.key, self.mode)  # type: ignore
        else:
            return AES.new(self.key, self.mode, self.iv)  # type: ignore

    def encrypt(self, dt: "data.Data") -> "data.Data":
        if not self.enable:
            return dt
        cipher = self.get_cipher()
        return data.Data(cipher.encrypt(dt.get_bytes()))

    def decrypt(self, dt: "data.Data") -> "data.Data":
        if not self.enable:
            return dt
        cipher = self.get_cipher()
        return data.Data(cipher.decrypt(dt.get_bytes()))

    @staticmethod
    def get_dat_cipher():
        return AesCipher(data.Data(Hash.get_decryption_key()).to_bytes())

    @staticmethod
    def decrypt_dat(dt: "data.Data") -> "data.Data":
        decrypted = AesCipher.get_dat_cipher().decrypt(dt[:-32])
        decrypted = decrypted.unpad_pkcs7() or decrypted
        return decrypted

    @staticmethod
    def encrypt_dat(dt: "data.Data", cc: str) -> "data.Data":
        try:
            dt = dt.pad_pkcs7()
        except ValueError:
            pass
        encrypted = AesCipher.get_dat_cipher().encrypt(dt)
        salt = data.Data(f"battlecats{cc}")

        file_hash = data.Data(
            Hash(HashAlgorithm.MD5, salt + encrypted).get_hash().to_hex()
        )
        return encrypted + file_hash


class Random:
    @staticmethod
    def get_bytes(length: int) -> bytes:
        return bytes(random.getrandbits(8) for _ in range(length))

    @staticmethod
    def get_alpha_string(length: int) -> str:
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(random.choice(characters) for _ in range(length))
