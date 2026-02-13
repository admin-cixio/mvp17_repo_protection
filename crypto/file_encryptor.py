"""
File Encryptor using AES-256-GCM
Handles encryption/decryption of repository files.
"""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
import base64


class FileEncryptor:
    """Encrypts and decrypts files using AES-256-GCM."""
    
    def __init__(self, encrypted_dir: str = "encrypted"):
        """
        Initialize FileEncryptor.
        
        Args:
            encrypted_dir: Directory to store encrypted files
        """
        self.encrypted_dir = Path(encrypted_dir)
        self.encrypted_dir.mkdir(exist_ok=True)
        self.manifest_path = self.encrypted_dir / "manifest.json"
        self.manifest: Dict = {}
    
    def generate_key(self, password: Optional[str] = None) -> bytes:
        """
        Generate AES-256 key.
        
        Args:
            password: Optional password for key derivation
            
        Returns:
            32-byte AES key
        """
        if password:
            # Derive key from password using scrypt
            salt = get_random_bytes(32)
            key = scrypt(password, salt, 32, N=2**14, r=8, p=1)
            return key, salt
        else:
            # Generate random key
            return get_random_bytes(32), None
    
    def encrypt_file(self, file_path: Path, key: bytes) -> Dict:
        """
        Encrypt a single file using AES-256-GCM.
        
        Args:
            file_path: Path to file to encrypt
            key: AES encryption key
            
        Returns:
            Dictionary with encryption metadata
        """
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                plaintext = f.read()
            
            # Create AES cipher
            cipher = AES.new(key, AES.MODE_GCM)
            
            # Encrypt
            ciphertext, tag = cipher.encrypt_and_digest(plaintext)
            
            # Create encrypted file path
            rel_path = file_path.relative_to('.')
            encrypted_path = self.encrypted_dir / f"{rel_path}.enc"
            encrypted_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Store nonce, tag, and ciphertext
            with open(encrypted_path, 'wb') as f:
                f.write(cipher.nonce)  # 16 bytes
                f.write(tag)           # 16 bytes
                f.write(ciphertext)
            
            return {
                'original_path': str(rel_path),
                'encrypted_path': str(encrypted_path),
                'size': len(plaintext),
                'encrypted_size': len(ciphertext) + 32,
                'status': 'success'
            }
        
        except Exception as e:
            return {
                'original_path': str(file_path),
                'status': 'error',
                'error': str(e)
            }
    
    def decrypt_file(self, encrypted_path: Path, key: bytes, output_path: Path) -> bool:
        """
        Decrypt a single file using AES-256-GCM.
        
        Args:
            encrypted_path: Path to encrypted file
            key: AES decryption key
            output_path: Path to save decrypted file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read encrypted file
            with open(encrypted_path, 'rb') as f:
                nonce = f.read(16)
                tag = f.read(16)
                ciphertext = f.read()
            
            # Create AES cipher
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            
            # Decrypt and verify
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            
            # Write decrypted file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(plaintext)
            
            return True
        
        except Exception as e:
            print(f"❌ Decryption failed for {encrypted_path}: {e}")
            return False
    
    def encrypt_repository(self, 
                          source_dir: str, 
                          file_list: List[Path],
                          key: Optional[bytes] = None) -> Dict:
        """
        Encrypt multiple files in repository.
        
        Args:
            source_dir: Source directory
            file_list: List of files to encrypt
            key: Encryption key (generated if not provided)
            
        Returns:
            Encryption statistics
        """
        if key is None:
            key, _ = self.generate_key()
        
        # Save key (encrypted with RSA in production)
        key_path = self.encrypted_dir / "aes_key.bin"
        with open(key_path, 'wb') as f:
            f.write(key)
        
        print(f"🔐 Encrypting {len(file_list)} files...")
        
        results = []
        success_count = 0
        error_count = 0
        
        for file_path in file_list:
            result = self.encrypt_file(file_path, key)
            results.append(result)
            
            if result['status'] == 'success':
                success_count += 1
                print(f"  ✅ {result['original_path']}")
            else:
                error_count += 1
                print(f"  ❌ {result['original_path']}: {result.get('error', 'Unknown error')}")
        
        # Save manifest
        self.manifest = {
            'encrypted_files': results,
            'total_files': len(file_list),
            'success_count': success_count,
            'error_count': error_count
        }
        
        with open(self.manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)
        
        print(f"\n📊 Encryption Summary:")
        print(f"   ✅ Success: {success_count}")
        print(f"   ❌ Errors: {error_count}")
        print(f"   📁 Manifest: {self.manifest_path}")
        
        return self.manifest
    
    def decrypt_repository(self, output_dir: str = ".") -> Dict:
        """
        Decrypt all files in encrypted directory.
        
        Args:
            output_dir: Output directory for decrypted files
            
        Returns:
            Decryption statistics
        """
        # Load manifest
        if not self.manifest_path.exists():
            print("❌ Manifest not found!")
            return {}
        
        with open(self.manifest_path, 'r') as f:
            self.manifest = json.load(f)
        
        # Load key
        key_path = self.encrypted_dir / "aes_key.bin"
        if not key_path.exists():
            print("❌ AES key not found!")
            return {}
        
        with open(key_path, 'rb') as f:
            key = f.read()
        
        print(f"🔓 Decrypting {self.manifest['total_files']} files...")
        
        success_count = 0
        error_count = 0
        
        for file_info in self.manifest['encrypted_files']:
            if file_info['status'] != 'success':
                continue
            
            encrypted_path = Path(file_info['encrypted_path'])
            output_path = Path(output_dir) / file_info['original_path']
            
            if self.decrypt_file(encrypted_path, key, output_path):
                success_count += 1
                print(f"  ✅ {file_info['original_path']}")
            else:
                error_count += 1
                print(f"  ❌ {file_info['original_path']}")
        
        print(f"\n📊 Decryption Summary:")
        print(f"   ✅ Success: {success_count}")
        print(f"   ❌ Errors: {error_count}")
        
        return {
            'success_count': success_count,
            'error_count': error_count
        }
    
    def search_encrypted(self, keyword: str, key: bytes) -> List[Dict]:
        """
        Search for keyword in encrypted files (requires decryption).
        
        Args:
            keyword: Keyword to search for
            key: Decryption key
            
        Returns:
            List of matches
        """
        if not self.manifest_path.exists():
            return []
        
        with open(self.manifest_path, 'r') as f:
            self.manifest = json.load(f)
        
        matches = []
        
        for file_info in self.manifest['encrypted_files']:
            if file_info['status'] != 'success':
                continue
            
            encrypted_path = Path(file_info['encrypted_path'])
            
            try:
                # Decrypt in memory
                with open(encrypted_path, 'rb') as f:
                    nonce = f.read(16)
                    tag = f.read(16)
                    ciphertext = f.read()
                
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                plaintext = cipher.decrypt_and_verify(ciphertext, tag)
                
                # Search for keyword
                if keyword.encode() in plaintext:
                    matches.append({
                        'file': file_info['original_path'],
                        'match': True
                    })
            
            except Exception as e:
                continue
        
        return matches


if __name__ == "__main__":
    # Demo usage
    encryptor = FileEncryptor()
    print("File Encryptor initialized")
