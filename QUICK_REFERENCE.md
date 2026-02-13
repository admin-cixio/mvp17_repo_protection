# Quick Reference: Edit Encrypted Code with Copilot

## The 3-Step Workflow

```
┌──────────────────────────────────────────────────────────┐
│  1. DECRYPT   →   2. EDIT   →   3. ENCRYPT               │
└──────────────────────────────────────────────────────────┘
```

### Step 1: Decrypt
```powershell
python edit_with_copilot.py web_app.py
```
Creates: `temp_edit/web_app.py` (Copilot can help here)

### Step 2: Edit
```powershell
code temp_edit/web_app.py
```
Use Copilot normally to make changes

### Step 3: Encrypt
```powershell
python save_encrypted.py web_app.py
```
Updates: `encrypted/web_app.py.enc`, deletes temp file

### Step 4: Test
```powershell
python run_local.py
```
Runs from encrypted code on http://localhost:5001

---

## Common Files

| File | Purpose |
|------|---------|
| `web_app.py` | Flask web application |
| `cli.py` | Command-line interface |
| `crypto/fhe_engine.py` | FHE operations |
| `crypto/file_encryptor.py` | Encryption logic |
| `crypto/key_manager.py` | Key management |

---

## Example: Add New Feature

```powershell
# 1. Decrypt
python edit_with_copilot.py web_app.py

# 2. Open and edit with Copilot
code temp_edit/web_app.py
# Add your code, use Copilot suggestions
# Save (Ctrl+S)

# 3. Re-encrypt
python save_encrypted.py web_app.py

# 4. Test
python run_local.py
# Visit http://localhost:5001
```

---

## What Copilot Sees

| Folder | Copilot | Your Code Protected? |
|--------|---------|----------------------|
| `source/` | ❌ **Hidden** | ✅ YES |
| `encrypted/` | ✅ Visible (but encrypted) | ✅ YES |
| `temp_edit/` | ✅ **Can help** | ⚠️ Temporary only |

**Result:** Copilot helps you, but your source code stays private!

---

## Pro Tips

1. **Edit one file at a time** - easier to track changes
2. **Always run save_encrypted.py** - don't leave temp files
3. **Test after every change** - restart with `python run_local.py`
4. **Use clear Copilot prompts** - "Add validation for..." works better than vague requests

---

## Troubleshooting

**"File not found"?**
```powershell
python edit_with_copilot.py
```
Shows available files

**Forgot to encrypt?**
```powershell
python save_encrypted.py web_app.py
```

**Need to start over?**
```powershell
Remove-Item -Recurse temp_edit
python edit_with_copilot.py web_app.py
```

---

## Full Documentation
See: `COPILOT_EDITING_GUIDE.md` for detailed examples
