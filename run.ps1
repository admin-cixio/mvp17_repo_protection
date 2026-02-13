# MVP17 Repository Protection - Helper Script
# Use this to run commands easily without typing the full Python path

$PYTHON = "C:/Users/Administrator/Desktop/work/CIXIO-REPOSITORIES/.venv/Scripts/python.exe"

Write-Host "`n🔐 MVP17 Repository Protection - Quick Commands" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

$command = $args[0]

if (-not $command) {
    Write-Host "`nUsage: .\run.ps1 <command>" -ForegroundColor Yellow
    Write-Host "`nAvailable commands:" -ForegroundColor Cyan
    Write-Host "  status   - Show protection status" -ForegroundColor Gray
    Write-Host "  encrypt  - Encrypt repository files" -ForegroundColor Gray
    Write-Host "  decrypt  - Decrypt repository files" -ForegroundColor Gray
    Write-Host "  search   - Search encrypted files" -ForegroundColor Gray
    Write-Host "  compute  - Run FHE computations" -ForegroundColor Gray
    Write-Host "  demo     - Run complete demo" -ForegroundColor Gray
    Write-Host "  hello    - Run hello world" -ForegroundColor Gray
    Write-Host "`nExamples:" -ForegroundColor Cyan
    Write-Host "  .\run.ps1 status" -ForegroundColor Gray
    Write-Host "  .\run.ps1 demo" -ForegroundColor Gray
    Write-Host "  .\run.ps1 encrypt" -ForegroundColor Gray
    Write-Host ""
    exit
}

switch ($command) {
    "status" {
        & $PYTHON main.py status
    }
    "encrypt" {
        & $PYTHON main.py encrypt
    }
    "decrypt" {
        & $PYTHON main.py decrypt
    }
    "search" {
        $keyword = $args[1]
        if ($keyword) {
            & $PYTHON main.py search $keyword
        } else {
            Write-Host "Usage: .\run.ps1 search <keyword>" -ForegroundColor Yellow
        }
    }
    "compute" {
        & $PYTHON main.py compute --operation demo
    }
    "demo" {
        & $PYTHON main.py demo
    }
    "hello" {
        & $PYTHON hello_world.py
    }
    "examples-search" {
        & $PYTHON examples/encrypted_search.py
    }
    "examples-compute" {
        & $PYTHON examples/encrypted_compute.py
    }
    "examples-copilot" {
        & $PYTHON examples/copilot_demo.py
    }
    default {
        Write-Host "Unknown command: $command" -ForegroundColor Red
        Write-Host "Run '.\run.ps1' without arguments to see available commands" -ForegroundColor Yellow
    }
}
