# MVP17: Repository Protection with Fully Homomorphic Encryption

## Overview
A POC/Demo implementation of repository protection using Fully Homomorphic Encryption (FHE) that allows operations on encrypted code without decryption.

## Features
- 🔐 **Hybrid Encryption**: RSA for keys + AES-256 for files + FHE for operations
- 🔑 **Key Management**: Public/Private key generation and management
- 📁 **Selective Encryption**: .repoignore file for excluding files (like .gitignore)
- 🔍 **Encrypted Search**: Search in encrypted files using FHE
- 🤖 **Copilot-Ready**: Work with encrypted codebase
- 📊 **FHE Operations**: Compute on encrypted data without decryption

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

## Project Structure
```
mvp17_repo_protection/
├── main.py                 # Main CLI interface
├── hello_world.py          # Demo hello world app
├── crypto/
│   ├── key_manager.py      # RSA key generation/management
│   ├── file_encryptor.py   # AES file encryption
│   └── fhe_engine.py       # FHE operations
├── utils/
│   ├── repoignore.py       # .repoignore parser
│   └── file_scanner.py     # Repository file scanner
├── examples/
│   ├── encrypted_search.py # Demo: Search encrypted files
│   ├── encrypted_compute.py# Demo: Compute on encrypted data
│   └── copilot_demo.py     # Demo: Copilot with encrypted code
├── .repoignore             # Files to exclude from encryption
├── keys/                   # Generated keys (gitignored)
│   ├── private_key.pem
│   └── public_key.pem
└── encrypted/              # Encrypted repository files
```

## License
MIT

## Author
CIXIO.DEV - MVP17 Team
