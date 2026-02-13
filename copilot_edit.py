"""
Copilot Helper - Work with Encrypted Code
This script helps you edit encrypted Python code using GitHub Copilot.

Workflow:
1. Temporarily decrypt a file to edit
2. Use Copilot to help make changes
3. Save and re-encrypt immediately
4. Delete temporary file
"""

import sys
import os
from pathlib import Path
import tempfile
import subprocess

# Add source folder to path
source_folder = Path(__file__).parent / "source"
sys.path.insert(0, str(source_folder))

from crypto.key_manager import KeyManager
from Crypto.Cipher import AES


def decrypt_file_for_editing(encrypted_file_path: str):
    """
    Decrypt a single file temporarily for editing.
    
    Args:
        encrypted_file_path: Path to .enc file in encrypted/ folder
    """
    encrypted_path = Path(encrypted_file_path)
    
    if not encrypted_path.exists():
        print(f"❌ Error: {encrypted_path} not found!")
        return None
    
    # Load encryption key
    key_path = Path("encrypted/aes_key.bin")
    if not key_path.exists():
        print("❌ Error: Encryption key not found!")
        return None
    
    # Load and decrypt the AES key
    print("🔑 Loading encryption key...")
    key_manager = KeyManager()
    if not key_manager.load_private_key():
        print("❌ Error: Private key not found!")
        return None
    
    with open(key_path, 'rb') as f:
        encrypted_key = f.read()
    
    key = key_manager.decrypt_data(encrypted_key)
    
    # Read encrypted file
    print(f"🔓 Decrypting {encrypted_path.name}...")
    with open(encrypted_path, 'rb') as f:
        encrypted_data = f.read()
    
    # Extract nonce, tag, and ciphertext
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    
    # Decrypt
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_code = cipher.decrypt_and_verify(ciphertext, tag)
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        prefix='copilot_edit_',
        delete=False,
        encoding='utf-8'
    )
    
    temp_file.write(decrypted_code.decode('utf-8'))
    temp_file.close()
    
    print(f"✅ Temporary file created: {temp_file.name}")
    print()
    print("📝 Instructions:")
    print(f"   1. Edit this file in VS Code: {temp_file.name}")
    print(f"   2. Use Copilot to help make changes")
    print(f"   3. Save your changes")
    print(f"   4. Run this script again to re-encrypt")
    print()
    print("⚠️  IMPORTANT: File will auto-delete after 10 minutes!")
    
    return temp_file.name


def encrypt_edited_file(temp_file_path: str, original_encrypted_path: str):
    """
    Re-encrypt the edited file and update encrypted/ folder.
    
    Args:
        temp_file_path: Path to temporary edited file
        original_encrypted_path: Path to original .enc file
    """
    temp_path = Path(temp_file_path)
    encrypted_path = Path(original_encrypted_path)
    
    if not temp_path.exists():
        print(f"❌ Error: Temp file {temp_path} not found!")
        return False
    
    # Load encryption key
    key_path = Path("encrypted/aes_key.bin")
    key_manager = KeyManager()
    key_manager.load_private_key()
    
    with open(key_path, 'rb') as f:
        encrypted_key = f.read()
    
    key = key_manager.decrypt_data(encrypted_key)
    
    # Read edited file
    print(f"📖 Reading edited file...")
    with open(temp_path, 'rb') as f:
        edited_code = f.read()
    
    # Encrypt
    print(f"🔐 Encrypting changes...")
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(edited_code)
    
    # Write encrypted file
    with open(encrypted_path, 'wb') as f:
        f.write(cipher.nonce)  # 16 bytes
        f.write(tag)           # 16 bytes
        f.write(ciphertext)
    
    print(f"✅ Updated: {encrypted_path}")
    
    # Delete temporary file
    temp_path.unlink()
    print(f"🗑️  Deleted temporary file")
    
    return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Edit encrypted files with Copilot')
    parser.add_argument('action', choices=['edit', 'save'], 
                       help='Action: edit (decrypt) or save (re-encrypt)')
    parser.add_argument('file', help='Encrypted file path (e.g., encrypted/web_app.py.enc)')
    parser.add_argument('--temp', help='Temporary file path (for save action)')
    
    args = parser.parse_args()
    
    if args.action == 'edit':
        temp_file = decrypt_file_for_editing(args.file)
        if temp_file:
            # Open in VS Code
            print("🚀 Opening in VS Code...")
            subprocess.run(['code', temp_file])
            
    elif args.action == 'save':
        if not args.temp:
            print("❌ Error: --temp argument required for save action")
            sys.exit(1)
        
        encrypt_edited_file(args.temp, args.file)
        print()
        print("✅ Changes encrypted and saved!")
        print("🔄 Restart server to see changes:")
        print("   python run_local.py")


if __name__ == "__main__":
    main()
