# Architecture Documentation

## System Overview

MVP17 Repository Protection is a proof-of-concept system that demonstrates Fully Homomorphic Encryption (FHE) applied to source code repositories. The system uses a hybrid approach combining multiple encryption techniques for security and performance.

## Architecture Layers

### 1. Key Management Layer
**Component**: `crypto/key_manager.py`

Handles RSA key pair generation and management:
- **RSA-4096**: Asymmetric encryption for key exchange
- **Private Key**: Used for decryption (must be kept secure)
- **Public Key**: Used for encryption (can be shared)

**Key Storage**:
```
keys/
├── private_key.pem  (600 permissions)
└── public_key.pem   (644 permissions)
```

### 2. File Encryption Layer
**Component**: `crypto/file_encryptor.py`

Implements fast symmetric encryption:
- **Algorithm**: AES-256-GCM
- **Mode**: Galois/Counter Mode (authenticated encryption)
- **Key Size**: 256 bits (32 bytes)
- **Nonce**: 128 bits (16 bytes) - unique per file
- **Tag**: 128 bits (16 bytes) - authentication tag

**Encryption Process**:
1. Generate random AES key
2. For each file:
   - Read plaintext
   - Generate unique nonce
   - Encrypt with AES-GCM
   - Store: nonce + tag + ciphertext
3. Store AES key (in production: encrypt with RSA public key)
4. Save manifest with file metadata

**File Format**:
```
[16 bytes: nonce][16 bytes: tag][N bytes: ciphertext]
```

### 3. FHE Computation Layer
**Component**: `crypto/fhe_engine.py`

Implements Fully Homomorphic Encryption using TenSEAL:
- **Library**: TenSEAL (Microsoft SEAL Python wrapper)
- **Scheme**: CKKS (approximate arithmetic on real numbers)
- **Alternative**: BFV (exact arithmetic on integers)

**FHE Parameters**:
- **Poly Modulus Degree**: 8192 (128-bit security)
- **Coefficient Modulus**: [60, 40, 40, 60] bits
- **Scale**: 2^40 for CKKS

**Supported Operations**:
- Addition (homomorphic)
- Multiplication (homomorphic)
- Summation (tree-based reduction)
- Mean calculation
- Polynomial evaluation

### 4. Selective Encryption Layer
**Component**: `utils/repoignore.py`

Implements .gitignore-like pattern matching:
- **Parser**: Uses pathspec library (GitWildMatch)
- **Patterns**: Supports glob patterns, negation, directories
- **Use Case**: Exclude keys, binaries, cache files

**Pattern Examples**:
```
keys/          # Exclude directory
*.pem          # Exclude by extension
!important.py  # Include exception
**/test/**     # Exclude nested test dirs
```

### 5. Repository Scanner
**Component**: `utils/file_scanner.py`

Scans repository for files to encrypt:
- Recursive directory traversal
- Extension filtering
- Size filtering (prevent huge files)
- Statistics collection

## Data Flow

### Encryption Flow
```
┌─────────────┐
│ Source Files│
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ File Scanner    │ ← Scan repository
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ .repoignore     │ ← Filter files
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Generate AES Key│ ← Random 256-bit key
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ AES-GCM Encrypt │ ← Encrypt each file
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Encrypted Files │ ← Store in encrypted/
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Save Manifest   │ ← Metadata
└─────────────────┘
```

### Decryption Flow
```
┌─────────────────┐
│ Load Manifest   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Load AES Key    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ For each file:  │
│ - Read nonce    │
│ - Read tag      │
│ - Read cipher   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ AES-GCM Decrypt │ ← Verify tag
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Write Plaintext │
└─────────────────┘
```

### FHE Computation Flow
```
┌─────────────────┐
│ Plaintext Data  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ FHE Encrypt     │ ← CKKS scheme
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Encrypted Vector│
└──────┬──────────┘
       │
       ▼
┌─────────────────────────────┐
│ Homomorphic Operations:     │
│ - Add encrypted vectors     │
│ - Multiply encrypted values │
│ - Sum encrypted array       │
│ - Compute on ciphertext     │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────┐
│ Encrypted Result│
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ FHE Decrypt     │ ← Only at end
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Plaintext Result│
└─────────────────┘
```

## Security Model

### Threat Model
**Protected Against**:
- ✅ Unauthorized file access (files are encrypted at rest)
- ✅ Data theft (encrypted data is useless without keys)
- ✅ Computation on sensitive data (FHE allows computation without decryption)

**Not Protected Against**:
- ❌ Private key compromise (attacker can decrypt everything)
- ❌ Side-channel attacks (timing, power analysis)
- ❌ Malicious code execution (sandbox required)
- ❌ Physical access to running system

### Key Security
**Private Key Protection**:
- Stored with 600 permissions (owner read/write only)
- Should be encrypted with password (not implemented in POC)
- Should be stored in HSM for production
- Never committed to version control

**AES Key Protection**:
- Randomly generated per encryption session
- In production: encrypt with RSA public key
- Store encrypted AES key alongside encrypted files
- Decrypt AES key with RSA private key when needed

### FHE Security
**Security Level**: ~128 bits (with poly modulus degree 8192)

**Properties**:
- Computations on encrypted data
- No intermediate decryption needed
- Result remains encrypted until explicitly decrypted
- Secure against ciphertext-only attacks

**Limitations**:
- High computational cost
- Noise accumulation (limits operation depth)
- Approximate results with CKKS scheme

## Performance Considerations

### AES-256-GCM
- **Speed**: ~1 GB/s (hardware accelerated)
- **Overhead**: ~32 bytes per file (nonce + tag)
- **Use Case**: Fast bulk encryption

### FHE Operations
- **Speed**: 100-1000x slower than plaintext operations
- **Memory**: 10-100x larger than plaintext
- **Use Case**: Privacy-preserving computation on sensitive data

### Optimization Strategies
1. **Selective Encryption**: Only encrypt sensitive files
2. **Batch Operations**: Process multiple files in parallel
3. **Caching**: Keep FHE context in memory
4. **Lazy Decryption**: Decrypt only when needed

## Integration Points

### Version Control (Git)
```
# Store encrypted files in Git
git add encrypted/

# Never commit keys
echo "keys/" >> .gitignore
echo "*.pem" >> .gitignore
```

### CI/CD Pipeline
```bash
# In CI: Decrypt for testing
python main.py decrypt --output ./workspace

# Run tests on decrypted code
pytest workspace/

# Re-encrypt if needed
python main.py encrypt
```

### Copilot Integration
```python
# Create temporary workspace
with EncryptedWorkspace() as workspace:
    # Edit files with Copilot
    # Changes are re-encrypted automatically
    pass
```

## Future Enhancements

### Production Readiness
- [ ] Password-protected private key
- [ ] Hardware Security Module (HSM) integration
- [ ] Encrypt AES key with RSA public key
- [ ] Multi-user key management
- [ ] Audit logging

### Performance
- [ ] Parallel file encryption
- [ ] Incremental encryption (only changed files)
- [ ] FHE operation caching
- [ ] GPU acceleration for FHE

### Features
- [ ] File-level access control
- [ ] Time-based decryption (expire access)
- [ ] Encrypted search index
- [ ] Encrypted version control
- [ ] Remote attestation

## References

- **TenSEAL**: https://github.com/OpenMined/TenSEAL
- **Microsoft SEAL**: https://github.com/microsoft/SEAL
- **AES-GCM**: NIST SP 800-38D
- **RSA**: RFC 8017 (PKCS #1)
