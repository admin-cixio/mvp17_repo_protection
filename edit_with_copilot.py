"""
SAFE COPILOT EDITING WORKFLOW
Edit encrypted Python files with Copilot assistance while keeping source private.

Workflow:
1. Decrypt encrypted file temporarily
2. Edit with Copilot in a temp location (Copilot CAN see this)
3. Save and re-encrypt immediately
4. Temp file auto-deleted

This way:
- source/ remains invisible to Copilot (protected)
- You get Copilot help on temporary decrypted files
- Changes go back to encrypted/ folder
- No permanent unencrypted files
"""

import sys
from pathlib import Path
from Crypto.Cipher import AES

# Add source folder to path
source_folder = Path(__file__).parent / "source"
sys.path.insert(0, str(source_folder))

from crypto.key_manager import KeyManager


def edit_encrypted_file(encrypted_file_rel_path: str):
    """
    Workflow to edit an encrypted file with Copilot.
    
    Args:
        encrypted_file_rel_path: e.g., "web_app.py" (will look in encrypted/)
    
    Example:
        python edit_with_copilot.py web_app.py
    """
    # Setup paths
    if not encrypted_file_rel_path.endswith('.enc'):
        encrypted_file_rel_path += '.enc'
    
    encrypted_path = Path(f"encrypted/{encrypted_file_rel_path}")
    
    if not encrypted_path.exists():
        print(f"❌ Error: {encrypted_path} not found!")
        print(f"\nAvailable files in encrypted/:")
        for f in Path("encrypted").rglob("*.py.enc"):
            print(f"   {f.relative_to('encrypted')}")
        return
    
    print("\n" + "="*60)
    print("🔐 SAFE COPILOT EDITING WORKFLOW")
    print("="*60)
    print()
    
    # Load and decrypt AES key
    print("🔑 Loading encryption key...")
    key_path = Path("encrypted/aes_key.bin")
    key_manager = KeyManager()
    key_manager.load_private_key()
    
    with open(key_path, 'rb') as f:
        encrypted_key = f.read()
    
    key = key_manager.decrypt_data(encrypted_key)
    
    # Decrypt the file
    print(f"🔓 Decrypting: {encrypted_path.name}")
    with open(encrypted_path, 'rb') as f:
        encrypted_data = f.read()
    
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_code = cipher.decrypt_and_verify(ciphertext, tag)
    
    # Create temp file in a Copilot-visible location
    temp_dir = Path("temp_edit")
    temp_dir.mkdir(exist_ok=True)
    
    original_name = encrypted_path.stem.replace('.enc', '')
    temp_file = temp_dir / f"{original_name}.py"
    
    with open(temp_file, 'wb') as f:
        f.write(decrypted_code)
    
    print(f"✅ Temporary file: {temp_file}")
    print()
    print("="*60)
    print("📝 NEXT STEPS:")
    print("="*60)
    print()
    print(f"1. Open in VS Code:")
    print(f"   code {temp_file}")
    print()
    print(f"2. Edit with Copilot assistance")
    print(f"   - Copilot CAN see this temp file")
    print(f"   - Make your changes")
    print(f"   - Save the file")
    print()
    print(f"3. Re-encrypt your changes:")
    print(f"   python save_encrypted.py {encrypted_file_rel_path}")
    print()
    print("="*60)
    print("⚠️  REMEMBER:")
    print("="*60)
    print("✅ source/ = Still invisible to Copilot (protected)")
    print("✅ temp_edit/ = Copilot can help you here")
    print("✅ Changes will be re-encrypted automatically")
    print("🗑️  temp_edit/ folder will be cleaned up after")
    print()


def save_edited_file(encrypted_file_rel_path: str):
    """
    Re-encrypt edited file and clean up temp.
    
    Args:
        encrypted_file_rel_path: e.g., "web_app.py" or "web_app.py.enc"
    """
    if not encrypted_file_rel_path.endswith('.enc'):
        encrypted_file_rel_path += '.enc'
    
    encrypted_path = Path(f"encrypted/{encrypted_file_rel_path}")
    original_name = encrypted_path.stem.replace('.enc', '')
    temp_file = Path("temp_edit") / f"{original_name}.py"
    
    if not temp_file.exists():
        print(f"❌ Error: {temp_file} not found!")
        print(f"   Run: python edit_with_copilot.py {encrypted_file_rel_path}")
        return
    
    print("\n" + "="*60)
    print("🔐 RE-ENCRYPTING EDITED FILE")
    print("="*60)
    print()
    
    # Load key
    print("🔑 Loading encryption key...")
    key_path = Path("encrypted/aes_key.bin")
    key_manager = KeyManager()
    key_manager.load_private_key()
    
    with open(key_path, 'rb') as f:
        encrypted_key = f.read()
    
    key = key_manager.decrypt_data(encrypted_key)
    
    # Read edited file
    print(f"📖 Reading: {temp_file}")
    with open(temp_file, 'rb') as f:
        edited_code = f.read()
    
    # Encrypt
    print(f"🔐 Encrypting changes...")
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(edited_code)
    
    # Save encrypted
    with open(encrypted_path, 'wb') as f:
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)
    
    print(f"✅ Saved: {encrypted_path}")
    
    # Clean up temp
    temp_file.unlink()
    print(f"🗑️  Deleted: {temp_file}")
    
    # Try to remove temp_edit directory if empty
    try:
        Path("temp_edit").rmdir()
        print(f"🗑️  Removed: temp_edit/")
    except:
        pass
    
    print()
    print("="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print()
    print("🔄 Restart server to see changes:")
    print("   python run_local.py")
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("\n" + "="*60)
        print("USAGE:")
        print("="*60)
        print()
        print("1. Edit encrypted file:")
        print("   python edit_with_copilot.py web_app.py")
        print()
        print("2. Save changes:")
        print("   python save_encrypted.py web_app.py")
        print()
        sys.exit(1)
    
    script_name = Path(sys.argv[0]).name
    file_to_edit = sys.argv[1]
    
    if 'edit_with_copilot' in script_name:
        edit_encrypted_file(file_to_edit)
    elif 'save_encrypted' in script_name:
        save_edited_file(file_to_edit)
    else:
        print("❌ Unknown script name")
