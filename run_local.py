"""
Run web application from ENCRYPTED source code for LOCAL development.
Even in local development, we run from encrypted code.
"""

import sys
from pathlib import Path

# Add source folder to path for utilities
source_folder = Path(__file__).parent / "source"
sys.path.insert(0, str(source_folder))

from crypto.key_manager import KeyManager

print("\n" + "="*60)
print("💻 MVP17 - LOCAL Development from ENCRYPTED Code")
print("="*60)
print()
print("� Mode: LOCAL DEVELOPMENT (Encrypted)")
print("📁 Source: encrypted/ folder")
print("� Security: AES-256-GCM + RSA-4096")
print("🌍 Environment: LOCAL")
print()
print("📱 Open your browser to: http://localhost:5001")
print()
print("⚠️  Note: Running from ENCRYPTED code!")
print("   Code is decrypted in-memory during execution.")
print()
print("🛑 Press Ctrl+C to stop the server")
print()

# Load encryption key
key_path = Path("encrypted/aes_key.bin")
if not key_path.exists():
    print("❌ Error: Encryption key not found!")
    print("   Please encrypt source code first:")
    print("   python manage_encryption.py encrypt")
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
    print("   Please encrypt source code first:")
    print("   python manage_encryption.py encrypt")
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
print("🚀 Starting LOCAL Flask server...")
print()

# Execute the decrypted code with modified port
# We'll modify the Flask app to run on port 5001 for local dev
exec_globals = {
    '__name__': '__main__',
    '__file__': str(encrypted_webapp),
    'LOCAL_DEV_MODE': True,
    'LOCAL_DEV_PORT': 5001
}

exec(decrypted_code, exec_globals)
