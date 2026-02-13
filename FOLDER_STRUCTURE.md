# Folder Structure Guide

This project has a clear separation between unencrypted and encrypted code.

## 📁 Folder Structure

```
mvp17_repo_protection/
├── source/                    # ✏️ UNENCRYPTED source code (edit here)
│   ├── crypto/               # Encryption modules
│   ├── utils/                # Utility modules
│   ├── examples/             # Example scripts
│   ├── main.py               # CLI application
│   ├── web_app.py            # Web application
│   └── hello_world.py        # Demo application
│
├── encrypted/                 # 🔐 ENCRYPTED code (generated, do not edit)
│   ├── crypto/               # Encrypted crypto modules
│   ├── utils/                # Encrypted utility modules
│   ├── examples/             # Encrypted examples
│   ├── main.py.enc           # Encrypted CLI
│   ├── web_app.py.enc        # Encrypted web app
│   ├── hello_world.py.enc    # Encrypted demo
│   ├── aes_key.bin           # Encrypted AES key (RSA encrypted)
│   └── manifest.json         # Encryption manifest
│
├── keys/                      # 🔑 Encryption keys (never commit!)
│   ├── private_key.pem       # RSA-4096 private key
│   ├── public_key.pem        # RSA-4096 public key
│   └── fhe_context.bin       # FHE context
│
├── templates/                 # 🌐 Web application templates
│   ├── index.html
│   ├── dashboard.html
│   └── demo.html
│
├── manage_encryption.py       # 🛠️ Encryption management script
├── run_encrypted_webapp.py    # 🚀 Run web app from encrypted code
└── .repoignore               # Exclusion patterns
```

## 🔄 Workflow

### 1. Edit Source Code
All development happens in the `source/` folder:
```bash
source/
  ├── web_app.py       # Edit this
  ├── main.py          # Edit this
  └── crypto/          # Edit modules here
```

### 2. Encrypt Source Code
After making changes, encrypt the source code:
```powershell
python manage_encryption.py encrypt
```

This will:
- ✅ Clear the `encrypted/` folder
- ✅ Encrypt all files from `source/` to `encrypted/`
- ✅ Generate AES-256-GCM encrypted versions
- ✅ Create manifest.json
- ✅ Store RSA-encrypted AES key

### 3. Run from Encrypted Code
Run the web application from encrypted code:
```powershell
python run_encrypted_webapp.py
```

This will:
- ✅ Load encrypted `web_app.py.enc`
- ✅ Decrypt it in-memory
- ✅ Execute without touching disk
- ✅ Start Flask server at http://localhost:5000

### 4. Check Status
View encryption status anytime:
```powershell
python manage_encryption.py status
```

## 🎯 Key Points

### ✏️ Source Folder (`source/`)
- **Purpose**: Original unencrypted source code
- **Edit**: YES - Make all changes here
- **Commit**: Optional (depends on your workflow)
- **Encrypt**: YES - Excluded from encryption by .repoignore

### 🔐 Encrypted Folder (`encrypted/`)
- **Purpose**: Encrypted versions of source code
- **Edit**: NO - Auto-generated, will be overwritten
- **Commit**: YES - This is the protected code
- **Encrypt**: NO - Already encrypted

### 🔑 Keys Folder (`keys/`)
- **Purpose**: RSA and FHE encryption keys
- **Edit**: NO - Auto-generated
- **Commit**: NO - Never commit private keys!
- **Backup**: YES - Keep secure backups

## 🚀 Quick Start

1. **First Time Setup**:
   ```powershell
   # Encrypt source code
   python manage_encryption.py encrypt
   ```

2. **Run Web App from Encrypted Code**:
   ```powershell
   # Run from encrypted version
   python run_encrypted_webapp.py
   ```

3. **Development Workflow**:
   ```powershell
   # 1. Edit files in source/
   # 2. Encrypt again
   python manage_encryption.py encrypt
   
   # 3. Run from encrypted code
   python run_encrypted_webapp.py
   ```

## 🔒 Security Notes

- `source/` contains **unencrypted** code - protect access to this folder
- `encrypted/` contains **encrypted** code - safe to distribute
- `keys/` contains **private keys** - NEVER commit or share
- Web app runs from **encrypted code** decrypted in-memory only

## 📊 Commands Summary

```powershell
# Encryption Management
python manage_encryption.py encrypt    # Encrypt source/ to encrypted/
python manage_encryption.py status     # Show encryption status

# Running Applications
python run_encrypted_webapp.py         # Web app from encrypted code
python source/main.py [command]        # CLI from source (unencrypted)

# Original CLI (if needed)
python source/main.py init             # Initialize encryption
python source/main.py status           # Show repository status
python source/main.py demo             # Run demo
```

## ⚠️ Important

- Always edit in `source/` folder, never in `encrypted/`
- Run `manage_encryption.py encrypt` after any source changes
- Use `run_encrypted_webapp.py` to demonstrate running from encrypted code
- Keep `keys/` folder secure and never commit it
