"""
Flask Web Application for MVP17 Repository Protection
Demonstrates running a web app from encrypted source code.
"""

from flask import Flask, render_template, jsonify, request
import os
from pathlib import Path
from crypto.key_manager import KeyManager
from crypto.file_encryptor import FileEncryptor
from crypto.fhe_engine import FHEEngine
from utils.repoignore import RepoIgnore
import json

app = Flask(__name__)

# Initialize components
km = KeyManager()
encryptor = FileEncryptor()
fhe = FHEEngine()
repoignore = RepoIgnore()


@app.route('/')
def index():
    """Home page showing encryption status."""
    return render_template('index.html')


@app.route('/api/status')
def api_status():
    """API endpoint for system status."""
    # Check keys
    keys_exist = km.keys_exist()
    
    # Check FHE context
    fhe_exists = Path(fhe.context_path).exists()
    
    # Check encrypted files
    encrypted_exists = Path('encrypted/manifest.json').exists()
    encrypted_count = 0
    
    if encrypted_exists:
        with open('encrypted/manifest.json', 'r') as f:
            manifest = json.load(f)
            encrypted_count = manifest.get('success_count', 0)
    
    # Check repoignore
    repoignore_exists = Path('.repoignore').exists()
    repoignore.load()
    pattern_count = len(repoignore.patterns)
    
    return jsonify({
        'rsa_keys': {
            'status': 'found' if keys_exist else 'missing',
            'private_key': str(km.private_key_path) if keys_exist else None,
            'public_key': str(km.public_key_path) if keys_exist else None
        },
        'fhe_context': {
            'status': 'found' if fhe_exists else 'missing',
            'path': str(fhe.context_path) if fhe_exists else None
        },
        'encrypted_files': {
            'status': 'found' if encrypted_exists else 'none',
            'count': encrypted_count
        },
        'repoignore': {
            'status': 'found' if repoignore_exists else 'missing',
            'patterns': pattern_count
        }
    })


@app.route('/api/encrypted-files')
def api_encrypted_files():
    """API endpoint to list encrypted files."""
    manifest_path = Path('encrypted/manifest.json')
    
    if not manifest_path.exists():
        return jsonify({'error': 'No encrypted files found'}), 404
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    files = []
    for file_info in manifest.get('encrypted_files', []):
        if file_info['status'] == 'success':
            files.append({
                'path': file_info['original_path'],
                'size': file_info['size'],
                'encrypted_size': file_info['encrypted_size']
            })
    
    return jsonify({'files': files, 'total': len(files)})


@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint to search in encrypted files."""
    keyword = request.json.get('keyword', '')
    
    if not keyword:
        return jsonify({'error': 'No keyword provided'}), 400
    
    # Load AES key
    key_path = Path('encrypted/aes_key.bin')
    if not key_path.exists():
        return jsonify({'error': 'Encryption key not found'}), 404
    
    with open(key_path, 'rb') as f:
        key = f.read()
    
    # Search
    matches = encryptor.search_encrypted(keyword, key)
    
    return jsonify({
        'keyword': keyword,
        'matches': matches,
        'count': len(matches)
    })


@app.route('/api/fhe-demo', methods=['POST'])
def api_fhe_demo():
    """API endpoint to run FHE operations."""
    operation = request.json.get('operation', 'sum')
    data = request.json.get('data', [1, 2, 3, 4, 5])
    
    # Load FHE context
    if not fhe.load_context():
        return jsonify({'error': 'FHE context not found'}), 404
    
    # Encrypt data
    enc_data = fhe.encrypt(data)
    
    # Perform operation
    if operation == 'sum':
        enc_result = fhe.sum_encrypted(enc_data)
        result = fhe.decrypt(enc_result)[0]
        expected = sum(data)
    elif operation == 'mean':
        enc_result = fhe.mean_encrypted(enc_data)
        result = fhe.decrypt(enc_result)[0]
        expected = sum(data) / len(data)
    else:
        return jsonify({'error': 'Unknown operation'}), 400
    
    return jsonify({
        'operation': operation,
        'input_data': data,
        'result': round(result, 2),
        'expected': round(expected, 2),
        'match': abs(result - expected) < 0.5,
        'message': 'Computation done on ENCRYPTED data!'
    })


@app.route('/dashboard')
def dashboard():
    """Dashboard page."""
    return render_template('dashboard.html')


@app.route('/demo')
def demo():
    """Demo page with FHE operations."""
    return render_template('demo.html')


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔐 MVP17 Repository Protection - Web Interface")
    print("="*60)
    print("\n🚀 Starting web server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("\n⚠️  Note: This web app is running from ENCRYPTED source code!")
    print("   The Python files are encrypted with AES-256-GCM.")
    print("\n🛑 Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
