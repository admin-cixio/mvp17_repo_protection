# MVP17: Cixio Repository Protection with Fully Homomorphic Encryption

## Overview
A POC/Demo implementation of repository protection using Fully Homomorphic Encryption (FHE) that allows operations on encrypted code without decryption.

## Features
- 🔐 **Hybrid Encryption**: RSA for keys + AES-256 for files + FHE for operations
- 🔑 **Key Management**: Public/Private key generation and management
- 📁 **Selective Encryption**: .repoignore file for excluding files (like .gitignore)
- 🔍 **Encrypted Search**: Search in encrypted files using FHE
- 🤖 **Copilot-Safe Editing**: Edit encrypted code with Copilot assistance while keeping source private
- 📊 **FHE Operations**: Compute on encrypted data without decryption
- 🌐 **Web Interface**: Flask-based dashboard for managing encrypted files

## Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Repository Protection                      │
├─────────────────────────────────────────────────────────────┤
│  1. RSA Key Management (Public/Private Keys)                 │
│  2. AES-256 File Encryption (Fast, Symmetric)                │
│  3. FHE Operations (TenSEAL for encrypted compute)           │
│  4. .repoignore Parser (Exclude files from encryption)       │
│  5. Encrypted Code Interface (Copilot integration)           │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack
- **Python 3.8+**
- **Cryptography**: RSA, AES-256-GCM
- **TenSEAL**: FHE operations (Microsoft SEAL Python wrapper)

## Installation
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Commands
```bash
# 1. Generate keys
python main.py init

# 2. Encrypt repository
python main.py encrypt

# 3. Decrypt repository
python main.py decrypt

# 4. Search encrypted files (FHE)
python main.py search "keyword"

# 5. Perform FHE operations
python main.py compute --operation sum
```

### Running the Web Application

#### Local Development (Port 5001)
```powershell
python run_local.py
```
Visit: http://localhost:5001

#### Production (Port 5000)
```powershell
python run_encrypted_webapp.py
```
Visit: http://localhost:5000

### 🔐 Editing Encrypted Code with Copilot

Want to use GitHub Copilot to edit your Python backend while keeping source code private?

**Quick 3-Step Workflow:**

```powershell
# 1. Decrypt for editing
python edit_with_copilot.py web_app.py

# 2. Edit with Copilot
code temp_edit/web_app.py
# Use Copilot to make changes, then save

# 3. Re-encrypt
python save_encrypted.py web_app.py

# 4. Test
python run_local.py
```

**What this does:**
- ✅ Keeps `source/` hidden from Copilot
- ✅ Creates temporary decrypted file for editing
- ✅ Copilot helps you edit the temp file
- ✅ Re-encrypts changes automatically
- ✅ Cleans up temp files

**Learn More:**
- 📖 [Complete Guide](COPILOT_EDITING_GUIDE.md) - Detailed examples and workflows
- 🎯 [Quick Reference](QUICK_REFERENCE.md) - Command cheat sheet
- 📊 [Visual Guide](VISUAL_GUIDE.md) - Diagrams and illustrations
- ✅ [Solution Overview](COPILOT_SOLUTION.md) - How it works

## Project Structure
```
mvp17_repo_protection/
├── main.py                      # Main CLI interface
├── cli.py                       # CLI commands
├── hello_world.py               # Demo hello world app
├── manage_encryption.py         # Encryption management
├── run_local.py                 # Local server launcher (port 5001)
├── run_encrypted_webapp.py      # Production launcher (port 5000)
├── edit_with_copilot.py         # 🔐 Decrypt file for Copilot editing
├── save_encrypted.py            # 🔐 Re-encrypt edited file
├── source/                      # ⛔ Hidden from Copilot & Git
│   ├── web_app.py               # Flask application (unencrypted)
│   ├── cli.py                   # CLI implementation
│   └── crypto/
│       ├── key_manager.py       # RSA key generation/management
│       ├── file_encryptor.py    # AES file encryption
│       └── fhe_engine.py        # FHE operations
├── encrypted/                   # ✅ Encrypted production code
│   ├── web_app.py.enc           # Encrypted Flask app
│   ├── cli.py.enc               # Encrypted CLI
│   ├── aes_key.bin              # RSA-encrypted AES key
│   └── crypto/
│       └── *.py.enc             # Encrypted modules
├── temp_edit/                   # ✅ Temporary Copilot workspace
│   └── *.py                     # Decrypted files for editing
├── templates/                   # Flask HTML templates
│   ├── index.html
│   ├── dashboard.html
│   └── demo.html
├── keys/                        # Generated keys (gitignored)
│   ├── private_key.pem
│   └── public_key.pem
├── .repoignore                  # Files to exclude from encryption
├── .gitignore                   # Git exclusions (source/, temp_edit/, keys/)
├── .vscode/
│   └── settings.json            # Copilot restrictions
└── docs/
    ├── COPILOT_SOLUTION.md      # 🔐 How to edit with Copilot
    ├── COPILOT_EDITING_GUIDE.md # 🔐 Detailed editing guide
    ├── QUICK_REFERENCE.md       # 🔐 Command cheat sheet
    └── VISUAL_GUIDE.md          # 🔐 Visual diagrams
```

## Security Architecture

### Three-Layer Protection

#### Layer 1: Source Code Protection
- `source/` folder is **hidden from GitHub Copilot** via `.vscode/settings.json`
- `source/` folder is **excluded from Git** via `.gitignore`
- Unencrypted code never committed or visible to Copilot

#### Layer 2: Encrypted Production Code
- All production code in `encrypted/` folder
- AES-256-GCM encryption with unique nonces
- RSA-4096 encrypted AES keys
- Safe to commit to Git (encrypted)

#### Layer 3: Controlled Copilot Access
- Temporary decrypt workflow via `edit_with_copilot.py`
- Copilot only sees files YOU explicitly decrypt
- Automatic cleanup after editing
- Auditable access trail

### Execution Flow

**Both Local (5001) and Production (5000):**
1. Load encrypted `.enc` files from `encrypted/`
2. Decrypt RSA-encrypted AES key
3. Decrypt code in-memory only
4. Execute without writing to disk
5. Never creates unencrypted files during execution

**Result:** Your code runs encrypted, stored encrypted, and only decrypted in-memory or when YOU explicitly choose.

## License
MIT

## Author
CIXIO.DEV - MVP17 Team
