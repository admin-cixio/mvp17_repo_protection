# User Guide: MVP17 Repository Protection

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Advanced Features](#advanced-features)
4. [Working with Copilot](#working-with-copilot)
5. [Troubleshooting](#troubleshooting)

## Getting Started

### Installation

1. **Clone or create the project**:
```bash
cd C:\Users\Administrator\Desktop\work\CIXIO-REPOSITORIES\CIXIO.DEV\mvp17_repo_protection
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python main.py --version
```

### Quick Start

Run the complete demo:
```bash
python main.py demo
```

This will:
- Generate encryption keys
- Setup FHE context
- Demonstrate FHE operations
- Show the hello world application

## Basic Usage

### 1. Initialize Protection

Generate keys and setup encryption:
```bash
python main.py init
```

This creates:
- `keys/private_key.pem` - Your private decryption key (KEEP SECURE!)
- `keys/public_key.pem` - Your public encryption key
- `keys/fhe_context.bin` - FHE computation context
- `.repoignore` - File exclusion patterns

⚠️ **IMPORTANT**: Back up your private key! If lost, encrypted data cannot be recovered.

### 2. Configure Exclusions

Edit `.repoignore` to exclude files from encryption:

```bash
# Edit exclusion patterns
notepad .repoignore
```

Example patterns:
```
# Keys (never encrypt these!)
keys/
*.pem

# Large files
*.mp4
*.zip

# Specific files
config/secrets.json
```

### 3. Encrypt Repository

Encrypt all files (respecting `.repoignore`):
```bash
python main.py encrypt
```

Options:
```bash
# Encrypt specific directory
python main.py encrypt --dir ./src

# Encrypt only Python files
python main.py encrypt --extensions .py

# Encrypt multiple types
python main.py encrypt --extensions .py,.js,.txt
```

After encryption:
- Original files remain unchanged
- Encrypted files stored in `encrypted/` directory
- Manifest created: `encrypted/manifest.json`

### 4. Decrypt Repository

Decrypt all files back to original location:
```bash
python main.py decrypt
```

Options:
```bash
# Decrypt to different location
python main.py decrypt --output ./decrypted
```

### 5. Check Status

View current protection status:
```bash
python main.py status
```

Shows:
- ✅ RSA Keys status
- ✅ FHE Context status
- ✅ .repoignore configuration
- ✅ Encrypted files count

## Advanced Features

### Search Encrypted Files

Search for keywords without full decryption:
```bash
# Search for a keyword
python main.py search "hello"

# Search for function definition
python main.py search "def main"

# Search for import
python main.py search "import"
```

**How it works**:
- Files are temporarily decrypted in memory
- Keyword matching performed
- Results returned without saving decrypted files

### FHE Computations

Perform computations on encrypted data:

```bash
# Run demo of all FHE operations
python main.py compute --operation demo

# Compute sum on encrypted data
python main.py compute --operation sum

# Compute mean on encrypted data
python main.py compute --operation mean

# Multiply encrypted vectors
python main.py compute --operation multiply
```

**What's happening**:
1. Data is encrypted using FHE
2. Operations performed on encrypted data (NO DECRYPTION!)
3. Only final result is decrypted

This is the core of Fully Homomorphic Encryption!

### Run Example Scripts

**Encrypted Search Example**:
```bash
python examples/encrypted_search.py "keyword"
```

**FHE Computation Examples**:
```bash
python examples/encrypted_compute.py
```

**Copilot Integration Demo**:
```bash
python examples/copilot_demo.py
```

## Working with Copilot

### Scenario: Edit Encrypted Code with Copilot

**Problem**: Your code is encrypted, but you need to edit it with Copilot assistance.

**Solution**: Use temporary decrypted workspace.

#### Method 1: Manual Workflow

```bash
# 1. Decrypt to temporary workspace
python main.py decrypt --output ./temp_workspace

# 2. Open in VS Code and edit with Copilot
code ./temp_workspace

# 3. After editing, re-encrypt
cd temp_workspace
python ../main.py encrypt

# 4. Clean up temporary files
cd ..
rm -rf temp_workspace
```

#### Method 2: Using Python Context Manager

```python
from examples.copilot_demo import EncryptedWorkspace

# This automatically handles encryption/decryption
with EncryptedWorkspace() as workspace:
    # Edit files in workspace
    # Copilot can assist here
    print(f"Edit files in: {workspace}")
    
    # When done, workspace is automatically re-encrypted
```

### Best Practices for Copilot

1. **Minimize Decryption Time**
   - Decrypt only when actively editing
   - Re-encrypt as soon as done

2. **Selective Decryption**
   - Decrypt only files you need to edit
   - Keep sensitive files encrypted

3. **Version Control**
   - Commit encrypted versions
   - Never commit decrypted code
   - Add to `.gitignore`:
     ```
     temp_workspace/
     decrypted/
     ```

4. **Secure Cleanup**
   - Always delete temporary decrypted files
   - Use secure delete if available:
     ```bash
     # Windows
     cipher /w:temp_workspace
     
     # Linux
     shred -vfz temp_workspace/*
     ```

## Workflow Examples

### Example 1: Daily Development

```bash
# Morning: Start work
python main.py decrypt --output ./workspace
code ./workspace

# ... work with Copilot throughout the day ...

# Evening: End work
cd workspace
python ../main.py encrypt
cd ..
rm -rf workspace
```

### Example 2: Team Collaboration

**Team Member A (has private key)**:
```bash
# Decrypt repository
python main.py decrypt

# Make changes
# ...

# Re-encrypt
python main.py encrypt

# Commit encrypted version
git add encrypted/
git commit -m "Updated encrypted code"
git push
```

**Team Member B (has private key)**:
```bash
# Pull changes
git pull

# Decrypt to work
python main.py decrypt
```

### Example 3: CI/CD Pipeline

```yaml
# .github/workflows/test.yml
name: Test Encrypted Code

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Decrypt code
        env:
          PRIVATE_KEY: ${{ secrets.PRIVATE_KEY }}
        run: |
          echo "$PRIVATE_KEY" > keys/private_key.pem
          python main.py decrypt --output ./workspace
      
      - name: Run tests
        run: pytest workspace/
      
      - name: Cleanup
        run: rm -rf workspace keys/private_key.pem
```

## Troubleshooting

### Problem: "Keys not found"

**Solution**:
```bash
python main.py init
```

### Problem: "Encrypted directory not found"

**Solution**:
```bash
# You need to encrypt first
python main.py encrypt
```

### Problem: "Decryption failed"

**Possible causes**:
1. Wrong private key
2. Corrupted encrypted files
3. Mismatched AES key

**Solution**:
```bash
# Check status
python main.py status

# Verify key files exist
ls keys/

# Re-initialize if needed (will lose access to old encrypted files!)
python main.py init --force
```

### Problem: "FHE operations too slow"

**Solutions**:
1. Reduce data size
2. Use simpler operations
3. Reduce poly modulus degree (less secure):
   ```python
   # In fhe_engine.py
   fhe.setup(poly_modulus_degree=4096)  # Faster but less secure
   ```

### Problem: "Import errors"

**Solution**:
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Verify installation
python -c "import tenseal; print('TenSEAL OK')"
python -c "from cryptography.fernet import Fernet; print('Cryptography OK')"
```

### Problem: "Permission denied" (Linux/Mac)

**Solution**:
```bash
# Fix private key permissions
chmod 600 keys/private_key.pem

# Fix script permissions
chmod +x main.py
```

## Security Checklist

- [ ] Private key backed up securely
- [ ] Private key has restrictive permissions (600)
- [ ] Private key NOT in version control
- [ ] `.gitignore` includes `keys/` and `*.pem`
- [ ] `.repoignore` excludes sensitive files
- [ ] Temporary decrypted files cleaned up
- [ ] Encrypted files committed to Git
- [ ] Team members have own private keys (for production)

## Performance Tips

1. **Exclude Large Files**: Add to `.repoignore`:
   ```
   *.mp4
   *.zip
   *.tar.gz
   ```

2. **Selective Encryption**: Only encrypt source code:
   ```bash
   python main.py encrypt --extensions .py,.js,.ts
   ```

3. **Parallel Processing**: For large repos, process files in batches

4. **SSD Storage**: FHE operations benefit from fast storage

## Getting Help

- **Documentation**: See `ARCHITECTURE.md` for technical details
- **Examples**: Check `examples/` directory
- **Issues**: File bugs on GitHub
- **Security**: Report security issues privately

## Next Steps

- Explore FHE operations: `python main.py compute --operation demo`
- Try encrypted search: `python main.py search "keyword"`
- Review examples: `python examples/encrypted_compute.py`
- Read architecture: `ARCHITECTURE.md`
