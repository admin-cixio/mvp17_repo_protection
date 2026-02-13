# MVP17 Repository Protection - Setup and Demo Script
# Run this script to set up and test the repository protection system

Write-Host "`n==============================================================" -ForegroundColor Cyan
Write-Host "  MVP17 Repository Protection - Setup & Demo" -ForegroundColor Cyan
Write-Host "  Fully Homomorphic Encryption for Code Repositories" -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan

# Set Python executable
$PYTHON = "C:/Users/Administrator/Desktop/work/CIXIO-REPOSITORIES/.venv/Scripts/python.exe"

Write-Host "`n[Step 1/5] Checking Python environment..." -ForegroundColor Yellow
& $PYTHON --version

Write-Host "`n[Step 2/5] Verifying dependencies..." -ForegroundColor Yellow
& $PYTHON -c "import cryptography; print('✓ cryptography')"
& $PYTHON -c "import Crypto; print('✓ pycryptodome')"
& $PYTHON -c "import click; print('✓ click')"
& $PYTHON -c "import rich; print('✓ rich')"
& $PYTHON -c "import numpy; print('✓ numpy')"

Write-Host "`n[Step 3/5] Testing hello_world.py..." -ForegroundColor Yellow
& $PYTHON hello_world.py

Write-Host "`n[Step 4/5] Running initialization..." -ForegroundColor Yellow
Write-Host "This will generate RSA keys and FHE context..." -ForegroundColor Gray
& $PYTHON main.py init

Write-Host "`n[Step 5/5] Running FHE demo..." -ForegroundColor Yellow
Write-Host "This demonstrates homomorphic operations on encrypted data..." -ForegroundColor Gray
& $PYTHON main.py compute --operation demo

Write-Host "`n==============================================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green

Write-Host "`n📋 What was created:" -ForegroundColor Cyan
Write-Host "  ✓ RSA-4096 keys in keys/ directory" -ForegroundColor Gray
Write-Host "  ✓ FHE context for homomorphic operations" -ForegroundColor Gray
Write-Host "  ✓ .repoignore file for selective encryption" -ForegroundColor Gray

Write-Host "`n🚀 Quick Commands:" -ForegroundColor Cyan
Write-Host "  python main.py status      - Check protection status" -ForegroundColor Gray
Write-Host "  python main.py encrypt     - Encrypt repository" -ForegroundColor Gray
Write-Host "  python main.py decrypt     - Decrypt repository" -ForegroundColor Gray
Write-Host "  python main.py search 'x'  - Search encrypted files" -ForegroundColor Gray
Write-Host "  python main.py demo        - Run full demo" -ForegroundColor Gray

Write-Host "`n📚 Documentation:" -ForegroundColor Cyan
Write-Host "  QUICKSTART.md      - Quick start guide" -ForegroundColor Gray
Write-Host "  USER_GUIDE.md      - Complete user manual" -ForegroundColor Gray
Write-Host "  ARCHITECTURE.md    - Technical details" -ForegroundColor Gray
Write-Host "  PROJECT_SUMMARY.md - Project overview" -ForegroundColor Gray

Write-Host "`n⚠️  Important Security Notes:" -ForegroundColor Yellow
Write-Host "  • NEVER commit keys/ directory to Git" -ForegroundColor Red
Write-Host "  • ALWAYS backup your private key securely" -ForegroundColor Red
Write-Host "  • This is a POC - not production-ready" -ForegroundColor Red

Write-Host "`n==============================================================" -ForegroundColor Cyan
Write-Host "  Ready to protect your repository!" -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host ""
