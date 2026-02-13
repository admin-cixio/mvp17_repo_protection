"""
Deploy to production from ENCRYPTED code.
This script prepares encrypted code for production deployment.
"""

import sys
import shutil
from pathlib import Path

def deploy_production():
    """Prepare encrypted code for production deployment."""
    print("\n" + "="*60)
    print("🚀 MVP17 - Production Deployment from Encrypted Code")
    print("="*60)
    print()
    
    # Check if encrypted folder exists
    encrypted_dir = Path("encrypted")
    if not encrypted_dir.exists() or not list(encrypted_dir.rglob("*.enc")):
        print("❌ Error: Encrypted code not found!")
        print()
        print("Please encrypt source code first:")
        print("  python manage_encryption.py encrypt")
        print()
        sys.exit(1)
    
    # Check manifest
    manifest_path = encrypted_dir / "manifest.json"
    if not manifest_path.exists():
        print("❌ Error: Encryption manifest not found!")
        print()
        print("Please re-encrypt source code:")
        print("  python manage_encryption.py encrypt")
        print()
        sys.exit(1)
    
    # Count encrypted files
    encrypted_files = list(encrypted_dir.rglob("*.enc"))
    print(f"✅ Found {len(encrypted_files)} encrypted files")
    print()
    
    # Create deployment package
    deploy_dir = Path("deploy")
    if deploy_dir.exists():
        print("🗑️  Cleaning previous deployment...")
        shutil.rmtree(deploy_dir)
    
    deploy_dir.mkdir(exist_ok=True)
    
    print("📦 Creating deployment package...")
    
    # Copy encrypted folder
    shutil.copytree(encrypted_dir, deploy_dir / "encrypted")
    print("   ✅ Copied encrypted code")
    
    # Copy templates
    if Path("templates").exists():
        shutil.copytree("templates", deploy_dir / "templates")
        print("   ✅ Copied templates")
    
    # Copy keys (for production, you'd use environment variables)
    print("   ⚠️  Keys: Use environment variables in production!")
    
    # Copy launcher
    shutil.copy("run_encrypted_webapp.py", deploy_dir / "run_encrypted_webapp.py")
    print("   ✅ Copied launcher script")
    
    # Copy requirements if exists
    if Path("requirements.txt").exists():
        shutil.copy("requirements.txt", deploy_dir / "requirements.txt")
        print("   ✅ Copied requirements.txt")
    
    # Create deployment README
    deploy_readme = deploy_dir / "DEPLOY_README.md"
    with open(deploy_readme, 'w') as f:
        f.write("""# MVP17 Production Deployment

## 🔐 Encrypted Code Package

This package contains ENCRYPTED source code ready for production deployment.

### 📦 Contents:
- `encrypted/` - Encrypted source code (AES-256-GCM)
- `templates/` - Web application templates
- `run_encrypted_webapp.py` - Production launcher
- `requirements.txt` - Python dependencies

### 🚀 Deployment Steps:

1. **Upload to server**:
   ```bash
   scp -r deploy/ user@server:/path/to/app/
   ```

2. **Install dependencies**:
   ```bash
   cd /path/to/app/deploy
   pip install -r requirements.txt
   ```

3. **Set up keys** (use environment variables or secure vault):
   ```bash
   # Copy keys securely (NOT in git!)
   mkdir keys
   # Transfer private_key.pem, public_key.pem securely
   ```

4. **Run production server**:
   ```bash
   # Using Gunicorn (recommended)
   gunicorn -w 4 -b 0.0.0.0:5000 run_encrypted_webapp:app
   
   # Or simple Python (development only)
   python run_encrypted_webapp.py
   ```

### 🔒 Security Notes:

- ✅ All source code is encrypted with AES-256-GCM
- ✅ Code is decrypted in-memory only during execution
- ⚠️ **NEVER commit private keys to git**
- ⚠️ Use environment variables for keys in production
- ⚠️ Set proper file permissions (600 for keys)

### 📊 Monitoring:

- Web interface: http://your-server:5000
- Health check: http://your-server:5000/api/status
- Logs: Check server logs for encryption/decryption events

### 🔄 Updates:

1. Update source code locally
2. Re-encrypt: `python manage_encryption.py encrypt`
3. Re-deploy: `python deploy_production.py`
4. Upload new package to server
5. Restart application

---

**Generated**: Production deployment package from encrypted code
**Security**: AES-256-GCM + RSA-4096
**Status**: Ready for deployment
""")
    print("   ✅ Created deployment README")
    
    print()
    print("="*60)
    print("✅ Production Deployment Package Ready!")
    print("="*60)
    print()
    print(f"📦 Package location: {deploy_dir.absolute()}")
    print(f"📄 Files included: {len(list(deploy_dir.rglob('*')))}")
    print()
    print("Next steps:")
    print("  1. Review: deploy/DEPLOY_README.md")
    print("  2. Test: cd deploy && python run_encrypted_webapp.py")
    print("  3. Deploy: Upload deploy/ folder to production server")
    print()
    print("⚠️  Security reminders:")
    print("  - Transfer keys securely (not in git)")
    print("  - Use environment variables for keys")
    print("  - Set restrictive file permissions")
    print("  - Enable HTTPS in production")
    print()


if __name__ == "__main__":
    deploy_production()
