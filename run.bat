@echo off
REM MVP17 Repository Protection - Quick Runner

set PYTHON=C:\Users\Administrator\Desktop\work\CIXIO-REPOSITORIES\.venv\Scripts\python.exe

if "%1"=="" (
    echo.
    echo Usage: run.bat [command]
    echo.
    echo Available commands:
    echo   status   - Show protection status
    echo   encrypt  - Encrypt repository
    echo   decrypt  - Decrypt repository
    echo   demo     - Run demo
    echo   hello    - Run hello world
    echo.
    goto :eof
)

if "%1"=="status" %PYTHON% main.py status
if "%1"=="encrypt" %PYTHON% main.py encrypt
if "%1"=="decrypt" %PYTHON% main.py decrypt
if "%1"=="demo" %PYTHON% main.py demo
if "%1"=="hello" %PYTHON% hello_world.py
if "%1"=="compute" %PYTHON% main.py compute --operation demo
