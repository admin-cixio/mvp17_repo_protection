"""
Key Manager for RSA Key Generation and Management
Handles public/private key pair generation and storage.
"""

import os
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from typing import Tuple, Optional


class KeyManager:
    """Manages RSA key pairs for repository encryption."""
    
    def __init__(self, keys_dir: str = "keys"):
        """
        Initialize KeyManager.
        
        Args:
            keys_dir: Directory to store keys (default: "keys")
        """
        self.keys_dir = Path(keys_dir)
        self.private_key_path = self.keys_dir / "private_key.pem"
        self.public_key_path = self.keys_dir / "public_key.pem"
        self.private_key = None
        self.public_key = None
    
    def generate_keys(self, key_size: int = 4096) -> Tuple[bytes, bytes]:
        """
        Generate RSA key pair.
        
        Args:
            key_size: Size of RSA key in bits (default: 4096)
            
        Returns:
            Tuple of (private_key_pem, public_key_pem)
        """
        print(f"🔑 Generating {key_size}-bit RSA key pair...")
        
        # Generate private key
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        
        # Generate public key
        self.public_key = self.private_key.public_key()
        
        # Serialize private key
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Serialize public key
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        print("✅ Key pair generated successfully!")
        return private_pem, public_pem
    
    def save_keys(self, private_pem: bytes, public_pem: bytes):
        """
        Save keys to files.
        
        Args:
            private_pem: Private key in PEM format
            public_pem: Public key in PEM format
        """
        # Create keys directory if it doesn't exist
        self.keys_dir.mkdir(exist_ok=True)
        
        # Save private key
        with open(self.private_key_path, 'wb') as f:
            f.write(private_pem)
        print(f"💾 Private key saved to: {self.private_key_path}")
        
        # Save public key
        with open(self.public_key_path, 'wb') as f:
            f.write(public_pem)
        print(f"💾 Public key saved to: {self.public_key_path}")
        
        # Set restrictive permissions (Windows)
        try:
            os.chmod(self.private_key_path, 0o600)
            print("🔒 Private key permissions set to 600")
        except Exception as e:
            print(f"⚠️  Warning: Could not set permissions: {e}")
    
    def load_private_key(self) -> Optional[rsa.RSAPrivateKey]:
        """
        Load private key from file.
        
        Returns:
            RSA private key object or None if not found
        """
        if not self.private_key_path.exists():
            print(f"❌ Private key not found at: {self.private_key_path}")
            return None
        
        with open(self.private_key_path, 'rb') as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
        
        print(f"✅ Private key loaded from: {self.private_key_path}")
        return self.private_key
    
    def load_public_key(self) -> Optional[rsa.RSAPublicKey]:
        """
        Load public key from file.
        
        Returns:
            RSA public key object or None if not found
        """
        if not self.public_key_path.exists():
            print(f"❌ Public key not found at: {self.public_key_path}")
            return None
        
        with open(self.public_key_path, 'rb') as f:
            self.public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        
        print(f"✅ Public key loaded from: {self.public_key_path}")
        return self.public_key
    
    def encrypt_data(self, data: bytes) -> bytes:
        """
        Encrypt data using public key (RSA).
        Note: RSA can only encrypt small amounts of data.
        Use this for encrypting AES keys, not large files.
        
        Args:
            data: Data to encrypt (max ~470 bytes for 4096-bit key)
            
        Returns:
            Encrypted data
        """
        if not self.public_key:
            self.load_public_key()
        
        encrypted = self.public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted
    
    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt data using private key (RSA).
        
        Args:
            encrypted_data: Encrypted data
            
        Returns:
            Decrypted data
        """
        if not self.private_key:
            self.load_private_key()
        
        decrypted = self.private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted
    
    def keys_exist(self) -> bool:
        """
        Check if keys already exist.
        
        Returns:
            True if both keys exist, False otherwise
        """
        return self.private_key_path.exists() and self.public_key_path.exists()
    
    def initialize(self, force: bool = False):
        """
        Initialize key management (generate and save keys).
        
        Args:
            force: Force regeneration even if keys exist
        """
        if self.keys_exist() and not force:
            print("⚠️  Keys already exist!")
            print(f"   Private key: {self.private_key_path}")
            print(f"   Public key: {self.public_key_path}")
            print("   Use --force to regenerate")
            return
        
        # Generate keys
        private_pem, public_pem = self.generate_keys()
        
        # Save keys
        self.save_keys(private_pem, public_pem)
        
        print("\n🎉 Key initialization complete!")
        print(f"   Private key: {self.private_key_path}")
        print(f"   Public key: {self.public_key_path}")
        print("\n⚠️  IMPORTANT: Keep your private key secure!")


if __name__ == "__main__":
    # Demo usage
    km = KeyManager()
    km.initialize()
