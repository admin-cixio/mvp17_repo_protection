"""
Launcher script to run the web application from ENCRYPTED code.
This script loads and executes encrypted Python files.
"""

import sys
from pathlib import Path

# Add encrypted folder to path
encrypted_folder = Path(__file__).parent / "encrypted"
sys.path.insert(0, str(encrypted_folder))

# Import the decryption utilities from source
source_folder = Path(__file__).parent / "source"
sys.path.insert(0, str(source_folder))

from crypto.key_manager import KeyManager
from crypto.file_encryptor import FileEncryptor

def run_from_encrypted():
    """Load and execute web_app.py from encrypted folder."""
    print("\n" + "="*60)
    print("🔐 MVP17 Repository Protection - Running from ENCRYPTED Code")
    print("="*60)
    print()
    
    # Load encryption key
    key_path = Path("encrypted/aes_key.bin")
    if not key_path.exists():
        print("❌ Error: Encryption key not found!")
        print("   Please run encryption first: python source/main.py encrypt")
        sys.exit(1)
    
    # Load and decrypt the AES key
    print("🔑 Loading encrypted AES key...")
    key_manager = KeyManager()
    if not key_manager.load_private_key():
        print("❌ Error: Private key not found!")
        sys.exit(1)
    
    with open(key_path, 'rb') as f:
        encrypted_key = f.read()
    
    key = key_manager.decrypt_data(encrypted_key)
    
    # Check if web_app.py is encrypted
    encrypted_webapp = Path("encrypted/web_app.py.enc")
    if not encrypted_webapp.exists():
        print("❌ Error: Encrypted web_app.py not found!")
        print("   Please run encryption first: python source/main.py encrypt")
        sys.exit(1)
    
    print("🔓 Loading encrypted web_app.py...")
    
    # Decrypt and execute web_app.py
    from Crypto.Cipher import AES
    
    # Read encrypted file
    with open(encrypted_webapp, 'rb') as f:
        encrypted_data = f.read()
    
    # Extract nonce, tag, and ciphertext
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    
    # Decrypt
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_code = cipher.decrypt_and_verify(ciphertext, tag)
    
    print("✅ Decrypted web application code")
    print("🚀 Starting Flask server...")
    print("📱 Open your browser to: http://localhost:5000")
    print()
    print("⚠️  Note: This web app is running from ENCRYPTED source code!")
    print("   The Python files are stored encrypted with AES-256-GCM.")
    print("   They are decrypted in-memory only when executed.")
    print()
    print("🛑 Press Ctrl+C to stop the server")
    print()
    
    # Execute the decrypted code
    exec(decrypted_code, {'__name__': '__main__', '__file__': str(encrypted_webapp)})


if __name__ == "__main__":
    run_from_encrypted()
