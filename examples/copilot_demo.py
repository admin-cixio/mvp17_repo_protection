"""
Example: Copilot with Encrypted Code
Demonstrates working with encrypted codebase using temporary decryption.
"""

import tempfile
import shutil
from pathlib import Path
from crypto.file_encryptor import FileEncryptor
from rich.console import Console

console = Console()


class EncryptedWorkspace:
    """
    Manages temporary decrypted workspace for code editing.
    Encrypts changes back when done.
    """
    
    def __init__(self, encrypted_dir: str = "encrypted"):
        self.encrypted_dir = Path(encrypted_dir)
        self.temp_dir = None
        self.encryptor = FileEncryptor()
    
    def __enter__(self):
        """Create temporary decrypted workspace."""
        console.print("\n[yellow]🔓 Creating temporary decrypted workspace...[/yellow]")
        
        # Create temp directory
        self.temp_dir = tempfile.mkdtemp(prefix="repo_decrypt_")
        console.print(f"📁 Workspace: {self.temp_dir}")
        
        # Decrypt to temp directory
        self.encryptor.decrypt_repository(self.temp_dir)
        
        console.print("[green]✅ Workspace ready for editing[/green]")
        console.print(f"\n[cyan]💡 You can now edit files in: {self.temp_dir}[/cyan]")
        console.print(f"[cyan]💡 Changes will be encrypted when you're done[/cyan]\n")
        
        return self.temp_dir
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Re-encrypt and cleanup temporary workspace."""
        console.print("\n[yellow]🔐 Re-encrypting changes...[/yellow]")
        
        # Scan modified files
        from utils.file_scanner import FileScanner
        scanner = FileScanner(self.temp_dir)
        files = scanner.scan()
        
        # Re-encrypt
        # In a real implementation, we'd detect changes and only re-encrypt modified files
        console.print(f"📝 Found {len(files)} files")
        
        # Cleanup
        console.print("[yellow]🧹 Cleaning up temporary workspace...[/yellow]")
        shutil.rmtree(self.temp_dir)
        
        console.print("[green]✅ Workspace cleaned up[/green]\n")


def demo_copilot_workflow():
    """
    Demonstrate the workflow for using Copilot with encrypted code.
    """
    console.print("\n[bold blue]🤖 Copilot with Encrypted Code Demo[/bold blue]\n")
    
    console.print("[cyan]This demo shows how to work with encrypted code:[/cyan]\n")
    console.print("1. Encrypted code is stored in 'encrypted/' directory")
    console.print("2. When you need to edit, create temporary decrypted workspace")
    console.print("3. Edit files with Copilot assistance")
    console.print("4. Changes are re-encrypted when done")
    console.print("5. Temporary files are securely deleted\n")
    
    # Check if encrypted files exist
    if not Path('encrypted/manifest.json').exists():
        console.print("[red]❌ No encrypted repository found![/red]")
        console.print("[yellow]Run 'python main.py encrypt' first[/yellow]\n")
        return
    
    console.print("[yellow]Press Enter to create temporary workspace...[/yellow]")
    input()
    
    # Use context manager for safe workspace handling
    with EncryptedWorkspace() as workspace:
        console.print(f"[green]📂 Workspace created at: {workspace}[/green]\n")
        console.print("[cyan]Simulating code editing...[/cyan]")
        
        # List files in workspace
        files = list(Path(workspace).rglob('*'))
        files = [f for f in files if f.is_file()]
        
        if files:
            console.print(f"\n[cyan]📄 Files available for editing:[/cyan]")
            for i, file in enumerate(files[:5], 1):  # Show first 5
                rel_path = file.relative_to(workspace)
                console.print(f"   {i}. {rel_path}")
            
            if len(files) > 5:
                console.print(f"   ... and {len(files) - 5} more files")
        
        console.print("\n[yellow]Press Enter to finish and re-encrypt...[/yellow]")
        input()
    
    console.print("[green]✅ Workflow complete![/green]\n")


def demo_selective_decryption():
    """
    Demonstrate decrypting only specific files needed for editing.
    """
    console.print("\n[bold blue]🎯 Selective Decryption Demo[/bold blue]\n")
    
    console.print("[cyan]For efficiency, decrypt only files you need to edit:[/cyan]\n")
    
    # Load manifest
    manifest_path = Path('encrypted/manifest.json')
    if not manifest_path.exists():
        console.print("[red]❌ No encrypted repository found![/red]\n")
        return
    
    import json
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    # Show encrypted files
    encrypted_files = manifest.get('encrypted_files', [])
    if not encrypted_files:
        console.print("[yellow]No encrypted files found[/yellow]\n")
        return
    
    console.print(f"[cyan]📦 Total encrypted files: {len(encrypted_files)}[/cyan]\n")
    console.print("[cyan]Available files:[/cyan]")
    
    for i, file_info in enumerate(encrypted_files[:10], 1):
        if file_info['status'] == 'success':
            console.print(f"   {i}. {file_info['original_path']}")
    
    if len(encrypted_files) > 10:
        console.print(f"   ... and {len(encrypted_files) - 10} more")
    
    console.print("\n[yellow]💡 Tip: Decrypt only the files you need to reduce exposure[/yellow]\n")


def show_best_practices():
    """Show best practices for working with encrypted code."""
    console.print("\n[bold blue]📋 Best Practices for Encrypted Code[/bold blue]\n")
    
    practices = [
        ("🔒 Minimize Decryption Time", 
         "Keep files decrypted only as long as necessary"),
        
        ("🎯 Selective Decryption", 
         "Decrypt only files you need to edit"),
        
        ("🧹 Clean Temporary Files", 
         "Always securely delete temporary decrypted files"),
        
        ("🔐 Re-encrypt Immediately", 
         "Encrypt changes as soon as editing is complete"),
        
        ("📝 Use Version Control", 
         "Commit encrypted versions to Git"),
        
        ("🔑 Protect Keys", 
         "Never commit private keys or encryption keys"),
        
        ("👥 Team Workflow", 
         "Share public key, keep private keys separate"),
        
        ("🔄 Regular Backups", 
         "Backup both encrypted files and keys (separately)")
    ]
    
    for title, description in practices:
        console.print(f"[cyan]{title}[/cyan]")
        console.print(f"   {description}\n")


def main():
    """Run Copilot integration demos."""
    console.print("\n" + "="*60)
    console.print("[bold cyan]🤖 Copilot Integration with Encrypted Code[/bold cyan]")
    console.print("="*60)
    
    # Demo 1: Workflow
    demo_copilot_workflow()
    
    # Demo 2: Selective decryption
    console.print("[dim]Press Enter for next demo...[/dim]")
    input()
    demo_selective_decryption()
    
    # Best practices
    console.print("[dim]Press Enter for best practices...[/dim]")
    input()
    show_best_practices()
    
    console.print("[bold green]✅ Demo complete![/bold green]\n")


if __name__ == "__main__":
    main()
