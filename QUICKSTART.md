# Quick Start Guide

## Installation & Setup

### 1. Navigate to Project Directory
```powershell
cd C:\Users\Administrator\Desktop\work\CIXIO-REPOSITORIES\CIXIO.DEV\mvp17_repo_protection
```

### 2. Install Dependencies
The project uses a virtual environment already configured. If you need to install dependencies:

```powershell
pip install -r requirements.txt
```

### 3. Run Demo
```powershell
python main.py demo
```

This will:
- Generate RSA keys (4096-bit)
- Setup FHE context
- Demonstrate homomorphic operations
- Show hello world application

## Quick Commands

### Initialize Protection
```powershell
python main.py init
```

### Encrypt Repository
```powershell
python main.py encrypt
```

### Decrypt Repository
```powershell
python main.py decrypt
```

### Search Encrypted Files
```powershell
python main.py search "keyword"
```

### FHE Computations
```powershell
# Run all FHE demos
python main.py compute --operation demo

# Specific operations
python main.py compute --operation sum
python main.py compute --operation mean
```

### Check Status
```powershell
python main.py status
```

## What's Included

### Core Features
1. **RSA Key Management** - 4096-bit keys for secure key exchange
2. **AES-256-GCM Encryption** - Fast symmetric encryption for files
3. **FHE Operations** - Compute on encrypted data without decryption
4. **`.repoignore`** - Gitignore-like file exclusion
5. **Encrypted Search** - Search without full decryption
6. **Copilot Integration** - Work with encrypted code

### File Structure
```
mvp17_repo_protection/
├── main.py                 # CLI interface
├── hello_world.py          # Demo application
├── crypto/
│   ├── key_manager.py      # RSA keys
│   ├── file_encryptor.py   # AES encryption
│   └── fhe_engine.py       # FHE operations
├── utils/
│   ├── repoignore.py       # File exclusion
│   └── file_scanner.py     # Repository scanner
├── examples/
│   ├── encrypted_search.py
│   ├── encrypted_compute.py
│   └── copilot_demo.py
├── keys/                   # Generated keys
├── encrypted/              # Encrypted files
├── .repoignore
├── .gitignore
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
└── USER_GUIDE.md
```

## Examples

### Example 1: Protect Your Code
```powershell
# Initialize
python main.py init

# Encrypt Python files only
python main.py encrypt --extensions .py

# Check what was encrypted
python main.py status
```

### Example 2: Work with Encrypted Code
```powershell
# Decrypt to temporary workspace
python main.py decrypt --output ./temp

# Edit files...
# Then re-encrypt
cd temp
python ../main.py encrypt
cd ..
rm -r temp
```

### Example 3: Search Encrypted Repository
```powershell
# Search for function definitions
python main.py search "def "

# Search for imports
python main.py search "import"

# Search for specific code
python main.py search "encrypt"
```

## Important Notes

⚠️ **Security**:
- **NEVER** commit private keys to Git
- **ALWAYS** backup your private key securely
- This is a POC/Demo - not production-ready

📝 **File Exclusion**:
- Edit `.repoignore` to exclude files from encryption
- Keys and encrypted directories are automatically excluded

🔒 **Keys Location**:
- Private key: `keys/private_key.pem`
- Public key: `keys/public_key.pem`
- FHE context: `keys/fhe_context.bin`

## Troubleshooting

### Keys not found
```powershell
python main.py init
```

### Cannot decrypt
Make sure you have the correct private key in `keys/private_key.pem`

### Import errors
```powershell
pip install --upgrade -r requirements.txt
```

## Learn More

- **Full Documentation**: See `README.md`
- **Architecture Details**: See `ARCHITECTURE.md`
- **User Guide**: See `USER_GUIDE.md`
- **Examples**: Check `examples/` directory

## Next Steps

1. ✅ Run the demo: `python main.py demo`
2. ✅ Review `.repoignore` for file exclusions
3. ✅ Encrypt your first repository: `python main.py encrypt`
4. ✅ Try FHE operations: `python main.py compute`
5. ✅ Read the full documentation

## Support

For questions or issues:
- Check `USER_GUIDE.md` for detailed instructions
- Review `ARCHITECTURE.md` for technical details
- Run `python main.py --help` for CLI options
