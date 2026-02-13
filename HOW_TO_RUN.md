# 🚀 Running MVP17 Commands

## Problem: Python Module Errors?

If you see errors like `ModuleNotFoundError: No module named 'click'`, it means you're using the wrong Python interpreter.

## ✅ Solution: Use the Helper Scripts

### Option 1: PowerShell Helper (Recommended)
```powershell
# Show available commands
.\run.ps1

# Run specific commands
.\run.ps1 status
.\run.ps1 demo
.\run.ps1 encrypt
.\run.ps1 decrypt
.\run.ps1 hello
.\run.ps1 compute
```

### Option 2: Batch File
```cmd
run.bat status
run.bat demo
run.bat encrypt
```

### Option 3: Full Python Path
```powershell
C:/Users/Administrator/Desktop/work/CIXIO-REPOSITORIES/.venv/Scripts/python.exe main.py status
```

---

## 📋 Quick Commands

### Check Status
```powershell
.\run.ps1 status
```

### Run Demo
```powershell
.\run.ps1 demo
```

### Encrypt Repository
```powershell
.\run.ps1 encrypt
```

### Decrypt Repository
```powershell
.\run.ps1 decrypt
```

### Search Encrypted Files
```powershell
.\run.ps1 search "keyword"
```

### Run Hello World
```powershell
.\run.ps1 hello
```

### FHE Computations
```powershell
.\run.ps1 compute
```

---

## 🔧 Why This Happens

The project uses a **virtual environment** located at:
```
C:\Users\Administrator\Desktop\work\CIXIO-REPOSITORIES\.venv\
```

When you type just `python`, Windows uses the system Python (which doesn't have the packages installed).

The helper scripts automatically use the correct Python interpreter from the virtual environment.

---

## 💡 Pro Tip: Activate Virtual Environment

Alternatively, activate the virtual environment first:

```powershell
# Activate venv
C:\Users\Administrator\Desktop\work\CIXIO-REPOSITORIES\.venv\Scripts\Activate.ps1

# Now you can use 'python' directly
python main.py status
python main.py demo
python main.py encrypt
```

---

## 🎯 Recommended: Use Helper Scripts

The easiest way is to use `.\run.ps1` which handles everything for you!
