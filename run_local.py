"""
Run web application from UNENCRYPTED source code.
Use this for local development, debugging, and testing.
"""

import sys
from pathlib import Path

# Add source folder to path
source_folder = Path(__file__).parent / "source"
sys.path.insert(0, str(source_folder))

print("\n" + "="*60)
print("💻 MVP17 - Running from UNENCRYPTED Source Code")
print("="*60)
print()
print("🔓 Mode: DEVELOPMENT (Unencrypted)")
print("📁 Source: source/ folder")
print("🐛 Debugging: ENABLED")
print("🌍 Environment: LOCAL")
print()
print("📱 Open your browser to: http://localhost:5001")
print()
print("⚠️  Note: This is for LOCAL development only!")
print("   Do NOT use this in production.")
print()
print("🛑 Press Ctrl+C to stop the server")
print()

# Import and run the web app from source
try:
    # Change to source directory for imports to work
    import os
    os.chdir(source_folder)
    sys.path.insert(0, str(source_folder.absolute()))
    
    # Import Flask app
    from web_app import app
    
    # Run on different port (5001) to avoid conflicts
    app.run(host='0.0.0.0', port=5001, debug=True)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("  1. Ensure all files are in source/ folder")
    print("  2. Check that dependencies are installed")
    print("  3. Verify Python environment is activated")
    sys.exit(1)
