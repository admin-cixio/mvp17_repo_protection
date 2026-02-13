"""
Helper script to manage source code encryption workflow.
This ensures clear separation between source/ and encrypted/ folders.
"""

import sys
import shutil
from pathlib import Path

# Add source folder to path
source_folder = Path(__file__).parent / "source"
sys.path.insert(0, str(source_folder))

from crypto.key_manager import KeyManager
from crypto.file_encryptor import FileEncryptor
from utils.file_scanner import FileScanner
from utils.repoignore import RepoIgnore


def encrypt_source_to_encrypted():
    """Encrypt all files from source/ folder to encrypted/ folder."""
    print("\n" + "="*60)
    print("🔐 Encrypting Source Code")
    print("="*60)
    print()
    
    # Initialize
    key_manager = KeyManager()
    encryptor = FileEncryptor()
    scanner = FileScanner()
    repoignore = RepoIgnore()
    
    # Load or create keys
    if not key_manager.load_private_key():
        print("⚠️  Keys not found, generating new RSA-4096 keys...")
        private_pem, public_pem = key_manager.generate_keys()
        key_manager.save_keys(private_pem, public_pem)
    else:
        key_manager.load_public_key()
    
    # Check if source folder exists
    source_dir = Path("source")
    if not source_dir.exists():
        print("❌ Error: source/ folder not found!")
        sys.exit(1)
    
    # Clear encrypted folder
    encrypted_dir = Path("encrypted")
    if encrypted_dir.exists():
        print("🗑️  Cleaning encrypted/ folder...")
        shutil.rmtree(encrypted_dir)
    encrypted_dir.mkdir(exist_ok=True)
    
    # Scan source folder
    print("📁 Scanning source/ folder...")
    files = []
    for file_path in source_dir.rglob("*"):
        if file_path.is_file() and not repoignore.is_ignored(str(file_path)):
            files.append(str(file_path))
    
    print(f"   Found {len(files)} files to encrypt")
    print()
    
    if not files:
        print("❌ No files found to encrypt!")
        sys.exit(1)
    
    # Generate AES key for file encryption
    aes_key, _ = encryptor.generate_key()
    
    # Encrypt each file
    manifest = {}
    success_count = 0
    
    for file_path in files:
        try:
            # Read file
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Encrypt using AES-256-GCM
            from Crypto.Cipher import AES
            cipher = AES.new(aes_key, AES.MODE_GCM)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            
            # Determine output path (preserve directory structure)
            relative_path = Path(file_path).relative_to(source_dir)
            output_path = encrypted_dir / f"{relative_path}.enc"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write encrypted file: [nonce][tag][ciphertext]
            with open(output_path, 'wb') as f:
                f.write(cipher.nonce)  # 16 bytes
                f.write(tag)           # 16 bytes
                f.write(ciphertext)
            
            manifest[str(relative_path)] = {
                'original': file_path,
                'encrypted': str(output_path),
                'size': len(data)
            }
            
            success_count += 1
            print(f"   ✅ {relative_path}")
            
        except Exception as e:
            print(f"   ❌ {file_path}: {e}")
    
    # Encrypt and save AES key using RSA
    encrypted_key = key_manager.encrypt_data(aes_key)
    key_path = encrypted_dir / "aes_key.bin"
    with open(key_path, 'wb') as f:
        f.write(encrypted_key)
    
    # Save manifest
    import json
    manifest_path = encrypted_dir / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print()
    print("="*60)
    print(f"✅ Encryption Complete!")
    print(f"   Encrypted {success_count}/{len(files)} files")
    print(f"   Source folder: source/")
    print(f"   Encrypted folder: encrypted/")
    print(f"   Manifest: {manifest_path}")
    print("="*60)
    print()
    print("📱 To run the web app from encrypted code:")
    print("   python run_encrypted_webapp.py")
    print()


def show_status():
    """Show current encryption status."""
    print("\n" + "="*60)
    print("📊 Encryption Status")
    print("="*60)
    print()
    
    source_dir = Path("source")
    encrypted_dir = Path("encrypted")
    
    # Check source folder
    if source_dir.exists():
        source_files = list(source_dir.rglob("*.py"))
        print(f"📁 Source folder: {len(source_files)} Python files")
    else:
        print("📁 Source folder: Not found")
    
    # Check encrypted folder
    if encrypted_dir.exists():
        encrypted_files = list(encrypted_dir.rglob("*.enc"))
        manifest_path = encrypted_dir / "manifest.json"
        print(f"🔐 Encrypted folder: {len(encrypted_files)} encrypted files")
        if manifest_path.exists():
            print(f"   Manifest: ✅ Found")
        else:
            print(f"   Manifest: ❌ Not found")
    else:
        print("🔐 Encrypted folder: Not found")
    
    # Check keys
    keys_dir = Path("keys")
    if keys_dir.exists():
        private_key = keys_dir / "private_key.pem"
        public_key = keys_dir / "public_key.pem"
        if private_key.exists() and public_key.exists():
            print(f"🔑 Keys: ✅ RSA-4096 keys found")
        else:
            print(f"🔑 Keys: ⚠️  Incomplete")
    else:
        print("🔑 Keys: ❌ Not found")
    
    print()
    print("="*60)
    print()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("\n" + "="*60)
        print("🔐 MVP17 Repository Protection - Encryption Manager")
        print("="*60)
        print()
        print("Usage:")
        print("  python manage_encryption.py encrypt   - Encrypt source/ to encrypted/")
        print("  python manage_encryption.py status    - Show encryption status")
        print()
        print("Folder Structure:")
        print("  source/      - Original unencrypted source code")
        print("  encrypted/   - Encrypted versions of source files")
        print("  keys/        - RSA encryption keys")
        print()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "encrypt":
        encrypt_source_to_encrypted()
    elif command == "status":
        show_status()
    else:
        print(f"❌ Unknown command: {command}")
        print("   Use: encrypt, status")
        sys.exit(1)


if __name__ == "__main__":
    main()
