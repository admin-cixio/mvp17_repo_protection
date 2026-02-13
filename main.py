"""
MVP17 Repository Protection - Main CLI
Command-line interface for repository encryption with FHE.
"""

import click
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from crypto.key_manager import KeyManager
from crypto.file_encryptor import FileEncryptor
from crypto.fhe_engine import FHEEngine
from utils.repoignore import RepoIgnore
from utils.file_scanner import FileScanner


console = Console()


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    🔐 MVP17 Repository Protection with Fully Homomorphic Encryption
    
    Protect your repository with encryption and perform operations on encrypted data.
    """
    pass


@cli.command()
@click.option('--force', is_flag=True, help='Force regeneration of keys')
def init(force):
    """
    Initialize repository protection (generate keys).
    
    Example:
        python main.py init
        python main.py init --force
    """
    console.print("\n[bold blue]🔐 Initializing Repository Protection[/bold blue]\n")
    
    # Generate RSA keys
    km = KeyManager()
    km.initialize(force=force)
    
    # Setup FHE context
    console.print("\n[bold blue]🔧 Setting up FHE Engine[/bold blue]\n")
    fhe = FHEEngine()
    fhe.setup(scheme="ckks")
    fhe.save_context()
    
    # Create .repoignore if it doesn't exist
    ri = RepoIgnore()
    ri.load()
    
    console.print("\n[bold green]✅ Initialization Complete![/bold green]")
    console.print("\n[yellow]Next steps:[/yellow]")
    console.print("  1. Review .repoignore to exclude files")
    console.print("  2. Run: python main.py encrypt")
    console.print("")


@cli.command()
@click.option('--dir', default='.', help='Directory to encrypt')
@click.option('--extensions', default='.py,.js,.txt,.md', help='File extensions to encrypt (comma-separated)')
def encrypt(dir, extensions):
    """
    Encrypt repository files.
    
    Example:
        python main.py encrypt
        python main.py encrypt --dir ./src --extensions .py,.js
    """
    console.print("\n[bold blue]🔐 Encrypting Repository[/bold blue]\n")
    
    # Parse extensions
    ext_list = [ext.strip() for ext in extensions.split(',')]
    
    # Scan files
    scanner = FileScanner(dir)
    files = scanner.scan(extensions=ext_list)
    scanner.print_stats()
    
    # Filter with .repoignore
    ri = RepoIgnore()
    ri.load()
    filtered_files = ri.filter_files(files)
    
    if not filtered_files:
        console.print("\n[yellow]⚠️  No files to encrypt![/yellow]")
        return
    
    # Confirm
    console.print(f"\n[yellow]About to encrypt {len(filtered_files)} files. Continue? [y/N][/yellow]", end=' ')
    if input().lower() != 'y':
        console.print("[red]Cancelled[/red]")
        return
    
    # Encrypt
    encryptor = FileEncryptor()
    result = encryptor.encrypt_repository(dir, filtered_files)
    
    console.print("\n[bold green]✅ Encryption Complete![/bold green]")
    console.print(f"   Encrypted files: {result['success_count']}")
    console.print(f"   Errors: {result['error_count']}")
    console.print("")


@cli.command()
@click.option('--output', default='.', help='Output directory for decrypted files')
def decrypt(output):
    """
    Decrypt repository files.
    
    Example:
        python main.py decrypt
        python main.py decrypt --output ./decrypted
    """
    console.print("\n[bold blue]🔓 Decrypting Repository[/bold blue]\n")
    
    # Check if encrypted directory exists
    if not Path('encrypted').exists():
        console.print("[red]❌ Encrypted directory not found![/red]")
        console.print("[yellow]Run 'python main.py encrypt' first[/yellow]")
        return
    
    # Decrypt
    encryptor = FileEncryptor()
    result = encryptor.decrypt_repository(output)
    
    console.print("\n[bold green]✅ Decryption Complete![/bold green]")
    console.print(f"   Decrypted files: {result.get('success_count', 0)}")
    console.print(f"   Errors: {result.get('error_count', 0)}")
    console.print("")


@cli.command()
@click.argument('keyword')
def search(keyword):
    """
    Search for keyword in encrypted files.
    
    Example:
        python main.py search "hello"
        python main.py search "def main"
    """
    console.print(f"\n[bold blue]🔍 Searching for: '{keyword}'[/bold blue]\n")
    
    # Load key
    key_path = Path('encrypted/aes_key.bin')
    if not key_path.exists():
        console.print("[red]❌ Encryption key not found![/red]")
        return
    
    with open(key_path, 'rb') as f:
        key = f.read()
    
    # Search
    encryptor = FileEncryptor()
    matches = encryptor.search_encrypted(keyword, key)
    
    if matches:
        console.print(f"[green]✅ Found {len(matches)} matches:[/green]\n")
        for match in matches:
            console.print(f"   📄 {match['file']}")
    else:
        console.print("[yellow]No matches found[/yellow]")
    
    console.print("")


@cli.command()
@click.option('--operation', type=click.Choice(['demo', 'sum', 'mean', 'multiply']), 
              default='demo', help='FHE operation to perform')
def compute(operation):
    """
    Perform FHE computations on encrypted data.
    
    Example:
        python main.py compute --operation demo
        python main.py compute --operation sum
    """
    console.print("\n[bold blue]🔬 FHE Computation[/bold blue]\n")
    
    # Load or create FHE context
    fhe = FHEEngine()
    if not fhe.load_context():
        console.print("[yellow]Creating new FHE context...[/yellow]")
        fhe.setup(scheme="ckks")
    
    if operation == 'demo':
        fhe.demo_operations()
    else:
        # Sample computation
        data = [1.5, 2.5, 3.5, 4.5, 5.5]
        console.print(f"📊 Input data: {data}")
        
        # Encrypt
        console.print("🔐 Encrypting...")
        enc_data = fhe.encrypt(data)
        
        # Perform operation
        if operation == 'sum':
            console.print("➕ Computing sum (encrypted)...")
            enc_result = fhe.sum_encrypted(enc_data)
            result = fhe.decrypt(enc_result)[0]
            console.print(f"[green]✅ Sum: {round(result, 2)}[/green]")
            console.print(f"   Expected: {sum(data)}")
        
        elif operation == 'mean':
            console.print("📈 Computing mean (encrypted)...")
            enc_result = fhe.mean_encrypted(enc_data)
            result = fhe.decrypt(enc_result)[0]
            console.print(f"[green]✅ Mean: {round(result, 2)}[/green]")
            console.print(f"   Expected: {round(sum(data)/len(data), 2)}")
        
        elif operation == 'multiply':
            data2 = [0.5, 1.0, 1.5, 2.0, 2.5]
            console.print(f"📊 Second data: {data2}")
            console.print("🔐 Encrypting...")
            enc_data2 = fhe.encrypt(data2)
            console.print("✖️  Computing multiplication (encrypted)...")
            enc_result = fhe.multiply_encrypted(enc_data, enc_data2)
            result = fhe.decrypt(enc_result)[:len(data)]
            console.print(f"[green]✅ Result: {[round(x, 2) for x in result]}[/green]")
            console.print(f"   Expected: {[round(a*b, 2) for a, b in zip(data, data2)]}")


@cli.command()
def status():
    """
    Show repository protection status.
    
    Example:
        python main.py status
    """
    console.print("\n[bold blue]📊 Repository Protection Status[/bold blue]\n")
    
    # Create table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="white")
    
    # Check RSA keys
    km = KeyManager()
    if km.keys_exist():
        table.add_row("RSA Keys", "✅ Found", f"{km.private_key_path}")
    else:
        table.add_row("RSA Keys", "❌ Missing", "Run: python main.py init")
    
    # Check FHE context
    fhe = FHEEngine()
    if Path(fhe.context_path).exists():
        table.add_row("FHE Context", "✅ Found", f"{fhe.context_path}")
    else:
        table.add_row("FHE Context", "❌ Missing", "Run: python main.py init")
    
    # Check .repoignore
    if Path('.repoignore').exists():
        ri = RepoIgnore()
        ri.load()
        table.add_row(".repoignore", "✅ Found", f"{len(ri.patterns)} patterns")
    else:
        table.add_row(".repoignore", "❌ Missing", "Will be created on init")
    
    # Check encrypted directory
    if Path('encrypted').exists():
        encryptor = FileEncryptor()
        if Path(encryptor.manifest_path).exists():
            import json
            with open(encryptor.manifest_path, 'r') as f:
                manifest = json.load(f)
            table.add_row("Encrypted Files", "✅ Found", 
                         f"{manifest['success_count']} files encrypted")
        else:
            table.add_row("Encrypted Files", "⚠️  Partial", "Directory exists but no manifest")
    else:
        table.add_row("Encrypted Files", "❌ None", "Run: python main.py encrypt")
    
    console.print(table)
    console.print("")


@cli.command()
def demo():
    """
    Run complete demo of repository protection.
    
    Example:
        python main.py demo
    """
    console.print(Panel.fit(
        "[bold cyan]🎯 MVP17 Repository Protection Demo[/bold cyan]\n\n"
        "This demo will:\n"
        "1. Initialize keys and FHE context\n"
        "2. Show FHE operations\n"
        "3. Demonstrate encryption workflow",
        border_style="blue"
    ))
    
    console.print("\n[yellow]Press Enter to start...[/yellow]")
    input()
    
    # Step 1: Initialize
    console.print("\n[bold]Step 1: Initialize[/bold]")
    km = KeyManager()
    if not km.keys_exist():
        km.initialize()
    else:
        console.print("✅ Keys already exist")
    
    # Step 2: FHE Demo
    console.print("\n[bold]Step 2: FHE Operations[/bold]")
    fhe = FHEEngine()
    if not fhe.load_context():
        fhe.setup(scheme="ckks")
        fhe.save_context()
    fhe.demo_operations()
    
    # Step 3: Show hello world
    console.print("\n[bold]Step 3: Hello World Application[/bold]")
    import hello_world
    hello_world.main()
    
    console.print("\n[bold green]✅ Demo Complete![/bold green]")
    console.print("\n[yellow]Try these commands:[/yellow]")
    console.print("  python main.py encrypt    - Encrypt repository")
    console.print("  python main.py decrypt    - Decrypt repository")
    console.print("  python main.py search     - Search encrypted files")
    console.print("  python main.py status     - Check status")
    console.print("")


def main():
    """Main entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
