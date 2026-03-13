# MVP17 Repository Protection (FHE) — Knowledge Base

> Source code protection using Fully Homomorphic Encryption (PoC)

## Quick Reference

| Property | Value |
|---|---|
| **Repo** | `CIXIO.DEV/mvp17_repo_protection` |
| **Type** | Code protection tool (CLI + web dashboard) |
| **Tech** | Python, Flask, Click, Rich, TenSEAL |
| **Port** | 5001 (local), 5000 (production) |
| **Database** | None (file-based encryption) |
| **Status** | In-progress / PoC |

## Architecture

```
source/
├── main.py          → Real CLI (Click commands)
├── web_app.py       → Real Flask dashboard
├── crypto/          → Crypto engine
└── utils/           → Helpers
crypto/
├── key_manager.py    → RSA-4096 key gen/management
├── file_encryptor.py → AES-256-GCM file encryption
└── fhe_engine.py     → TenSEAL FHE operations
```

**Note:** Root `main.py` & `web_app.py` are empty stubs — real code in `source/`.

## Key Features

- RSA-4096 + AES-256-GCM file encryption
- Fully Homomorphic Encryption (TenSEAL/Microsoft SEAL) for encrypted search/compute
- `.repoignore` parser (like `.gitignore`) for selective encryption
- Copilot-safe editing workflow (decrypt → edit → re-encrypt)
- Flask web dashboard for encryption status

## CLI Commands

| Command | Purpose |
|---|---|
| `init` | Generate RSA keys |
| `encrypt` | Encrypt repo files |
| `decrypt` | Decrypt files |
| `search` | FHE encrypted search |
| `compute` | FHE operations on encrypted data |

## Dependencies

cryptography, pycryptodome, tenseal, click, rich, colorama, pathspec, watchdog, numpy

## Copilot Workflow

1. `edit_with_copilot.py` — decrypt file for editing
2. Edit with Copilot/IDE
3. `save_encrypted.py` — re-encrypt after editing
