# 🚀 MVP17 Repository Protection - Complete Workflow Guide

## 📁 Folder Structure

```
mvp17_repo_protection/
│
├── source/                    # ✏️ UNENCRYPTED - Development & Editing
│   ├── crypto/               # Encryption modules
│   ├── utils/                # Utility modules  
│   ├── examples/             # Example scripts
│   ├── web_app.py            # Flask web application
│   ├── main.py               # CLI application
│   └── hello_world.py        # Demo application
│
├── encrypted/                 # 🔐 ENCRYPTED - Production Ready
│   ├── crypto/               # Encrypted modules (.enc files)
│   ├── utils/                # Encrypted utilities (.enc files)
│   ├── examples/             # Encrypted examples (.enc files)
│   ├── web_app.py.enc        # Encrypted Flask app
│   ├── main.py.enc           # Encrypted CLI
│   ├── aes_key.bin           # RSA-encrypted AES key
│   └── manifest.json         # Encryption manifest
│
├── deploy/                    # 📦 DEPLOYMENT - Production Package
│   ├── encrypted/            # Copy of encrypted code
│   ├── templates/            # Web templates
│   ├── run_encrypted_webapp.py
│   └── DEPLOY_README.md      # Deployment instructions
│
├── keys/                      # 🔑 Encryption Keys (NEVER COMMIT!)
│   ├── private_key.pem       # RSA-4096 private key
│   ├── public_key.pem        # RSA-4096 public key
│   └── fhe_context.bin       # FHE context
│
├── templates/                 # 🌐 Web Templates
│   ├── index.html
│   ├── dashboard.html
│   └── demo.html
│
├── run_local.py              # 💻 Run from UNENCRYPTED code (DEV)
├── run_encrypted_webapp.py   # 🔐 Run from ENCRYPTED code (PROD)
├── manage_encryption.py      # 🔄 Encrypt source to encrypted
├── deploy_production.py      # 🚀 Create production package
└── WORKFLOW.md               # 📖 This file
```

---

## 🔄 Complete Workflow

### 1️⃣ Local Development (Unencrypted)

**Purpose**: Edit, debug, and test code locally

```powershell
# Edit source files
code source/web_app.py
code source/crypto/fhe_engine.py

# Run locally from unencrypted code
python run_local.py
```

- **Port**: `http://localhost:5001`
- **Mode**: Development (Debug enabled)
- **Source**: `source/` folder (unencrypted)
- **Hot reload**: ✅ Enabled
- **Debugging**: ✅ Full access

**Use this when:**
- ✅ Developing new features
- ✅ Debugging issues
- ✅ Testing changes quickly
- ✅ Verifying functionality

---

### 2️⃣ Encrypt Source Code

**Purpose**: Convert source code to encrypted format

```powershell
# Encrypt all files from source/ to encrypted/
python manage_encryption.py encrypt

# Check encryption status
python manage_encryption.py status
```

**What happens:**
- ✅ Clears `encrypted/` folder
- ✅ Encrypts all files from `source/` with AES-256-GCM
- ✅ Stores encrypted files as `.enc` in `encrypted/`
- ✅ Generates RSA-encrypted AES key
- ✅ Creates manifest.json

**Run this:**
- 🔄 After making changes to source code
- 🔄 Before running from encrypted code
- 🔄 Before creating production deployment
- 🔄 Before committing to GitHub

---

### 3️⃣ Test Encrypted Code Locally

**Purpose**: Verify encrypted code works correctly

```powershell
# Run from encrypted code
python run_encrypted_webapp.py
```

- **Port**: `http://localhost:5000`
- **Mode**: Production-like (from encrypted)
- **Source**: `encrypted/` folder (AES-256-GCM encrypted)
- **Decryption**: In-memory only
- **Debugging**: Limited

**Use this when:**
- ✅ Testing encrypted code execution
- ✅ Verifying encryption worked correctly
- ✅ Simulating production environment
- ✅ Final testing before deployment

---

### 4️⃣ Create Production Package

**Purpose**: Prepare encrypted code for deployment

```powershell
# Create deployment package
python deploy_production.py
```

**What happens:**
- ✅ Creates `deploy/` folder
- ✅ Copies encrypted code
- ✅ Copies templates
- ✅ Copies launcher script
- ✅ Generates deployment README

**Output**: `deploy/` folder ready for production

---

### 5️⃣ Deploy to Production

**Purpose**: Deploy encrypted code to server

```bash
# On local machine - create package
python deploy_production.py

# Upload to server
scp -r deploy/ user@server:/path/to/app/

# On server - install dependencies
cd /path/to/app/deploy
pip install -r requirements.txt

# Securely transfer keys (NOT in git!)
mkdir keys
# Copy private_key.pem and public_key.pem securely

# Run production server
gunicorn -w 4 -b 0.0.0.0:5000 run_encrypted_webapp:app
```

---

## 🎯 Quick Commands Reference

### Development
```powershell
# Run locally (unencrypted)
python run_local.py                    # Port 5001, debug mode

# Edit source code
code source/web_app.py                 # Edit any file in source/
```

### Encryption
```powershell
# Encrypt source code
python manage_encryption.py encrypt    # source/ → encrypted/

# Check status
python manage_encryption.py status     # Show encryption status
```

### Testing
```powershell
# Test encrypted code locally
python run_encrypted_webapp.py         # Port 5000, production-like
```

### Deployment
```powershell
# Create production package
python deploy_production.py            # Creates deploy/ folder

# Deploy to server
scp -r deploy/ user@server:/app/       # Upload package
```

---

## 🔐 GitHub Copilot with Encrypted Code

### Using Copilot with Encrypted Codebase

**For analysis and search in encrypted code:**

1. **Commit encrypted code to GitHub**:
   ```powershell
   git add encrypted/
   git commit -m "Update encrypted codebase"
   git push
   ```

2. **Use Copilot Chat**:
   - Copilot will have access to `encrypted/` folder in your repo
   - Can reference encrypted files for context
   - Understands the encryption structure

3. **For editing, work in source/**:
   ```powershell
   # Edit in source/ (unencrypted)
   code source/web_app.py
   
   # Then encrypt
   python manage_encryption.py encrypt
   
   # Commit encrypted version
   git add encrypted/
   git commit -m "Update encrypted code"
   ```

### Copilot Workflow

```
1. Edit → source/ (unencrypted, private)
2. Encrypt → python manage_encryption.py encrypt
3. Commit → encrypted/ (encrypted, can be public)
4. Copilot → Uses encrypted/ for analysis
5. Deploy → From encrypted/ folder
```

---

## 📊 Comparison Table

| Feature | Local (Unencrypted) | Encrypted Testing | Production |
|---------|---------------------|-------------------|------------|
| **Command** | `python run_local.py` | `python run_encrypted_webapp.py` | Deploy from `deploy/` |
| **Port** | 5001 | 5000 | 5000 (configurable) |
| **Source** | `source/` | `encrypted/` | `deploy/encrypted/` |
| **Encryption** | ❌ None | ✅ AES-256-GCM | ✅ AES-256-GCM |
| **Debug Mode** | ✅ Enabled | ✅ Enabled | ❌ Disabled |
| **Hot Reload** | ✅ Yes | ✅ Yes | ❌ No |
| **Use Case** | Development | Testing | Production |
| **Commit to Git** | ⚠️ Optional | ✅ Recommended | ✅ Yes |

---

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Edit code in `source/` folder
- ✅ Encrypt before committing: `python manage_encryption.py encrypt`
- ✅ Commit `encrypted/` folder to git
- ✅ Use `run_local.py` for development
- ✅ Use `run_encrypted_webapp.py` for testing encrypted code
- ✅ Deploy from `deploy/` folder
- ✅ Keep `keys/` folder secure and backed up
- ✅ Use environment variables for keys in production

### ❌ DON'T:
- ❌ DON'T commit `source/` folder to public repos
- ❌ DON'T commit `keys/` folder to git
- ❌ DON'T edit files in `encrypted/` folder directly
- ❌ DON'T use `run_local.py` in production
- ❌ DON'T share private keys
- ❌ DON'T skip encryption before deploying

---

## 🚦 Status Indicators

### Check Current Status:
```powershell
python manage_encryption.py status
```

**Output example:**
```
📁 Source folder: 14 Python files
🔐 Encrypted folder: 14 encrypted files
   Manifest: ✅ Found
🔑 Keys: ✅ RSA-4096 keys found
```

---

## 🐛 Troubleshooting

### Issue: "Encryption key not found"
```powershell
# Solution: Encrypt source code first
python manage_encryption.py encrypt
```

### Issue: "Source folder not found"
```powershell
# Solution: Ensure files are in source/ folder
ls source/
```

### Issue: "Import errors when running"
```powershell
# Solution: Check Python environment
C:\Users\Administrator\Desktop\work\CIXIO-REPOSITORIES\.venv\Scripts\python.exe --version

# Or activate virtual environment
.venv\Scripts\activate
python run_local.py
```

### Issue: "Port already in use"
```powershell
# Local dev uses port 5001
# Encrypted testing uses port 5000
# Check which is running and stop if needed
```

---

## 📝 Daily Development Workflow

### Morning - Start Development
```powershell
# 1. Pull latest changes
git pull

# 2. Run local dev server
python run_local.py

# 3. Open in browser: http://localhost:5001

# 4. Edit source code
code source/
```

### Afternoon - Test Changes
```powershell
# 1. Encrypt changes
python manage_encryption.py encrypt

# 2. Test encrypted version
python run_encrypted_webapp.py

# 3. Verify: http://localhost:5000
```

### Evening - Commit & Deploy
```powershell
# 1. Check status
python manage_encryption.py status

# 2. Commit encrypted code
git add encrypted/
git commit -m "Update: [describe changes]"
git push

# 3. Create deployment package
python deploy_production.py

# 4. Deploy to server
scp -r deploy/ user@server:/app/
```

---

## 🎓 Summary

| Step | Command | Purpose |
|------|---------|---------|
| **1. Edit** | `code source/` | Develop in unencrypted code |
| **2. Run Local** | `python run_local.py` | Test locally (port 5001) |
| **3. Encrypt** | `python manage_encryption.py encrypt` | Convert to encrypted |
| **4. Test Encrypted** | `python run_encrypted_webapp.py` | Test encrypted code (port 5000) |
| **5. Deploy** | `python deploy_production.py` | Create production package |
| **6. Commit** | `git add encrypted/ && git commit` | Save encrypted version |

---

## 🌟 Key Benefits

✅ **Clear Separation**: Unencrypted for dev, encrypted for production  
✅ **Easy Testing**: Test both versions locally  
✅ **Secure Deployment**: Always deploy from encrypted code  
✅ **Copilot Ready**: Encrypted code in git for Copilot analysis  
✅ **Debugging**: Full access in unencrypted mode  
✅ **Production Ready**: Encrypted code with deployment package  

---

**For more details, see:**
- `FOLDER_STRUCTURE.md` - Detailed folder structure
- `deploy/DEPLOY_README.md` - Production deployment guide
- `README.md` - Project overview
