"""
Key Management for Replay Signing.
Uses Ed25519 for deterministic digital signatures.
"""

import os
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization


class KeyManager:

    PRIVATE_KEY_PATH = "replay_private_key.pem"
    PUBLIC_KEY_PATH = "replay_public_key.pem"

    @classmethod
    def generate_keys(cls):
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()

        # Save private key
        with open(cls.PRIVATE_KEY_PATH, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        # Save public key
        with open(cls.PUBLIC_KEY_PATH, "wb") as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )

    @classmethod
    def load_private_key(cls):
        with open(cls.PRIVATE_KEY_PATH, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    @classmethod
    def load_public_key(cls):
        with open(cls.PUBLIC_KEY_PATH, "rb") as f:
            return serialization.load_pem_public_key(f.read())