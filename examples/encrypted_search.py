"""
Example: Search in Encrypted Files
Demonstrates searching for keywords in encrypted repository without full decryption.
"""

from pathlib import Path
from crypto.file_encryptor import FileEncryptor
from rich.console import Console

console = Console()


def search_encrypted_repository(keyword: str):
    """
    Search for keyword in encrypted files.
    
    Args:
        keyword: Keyword to search for
    """
    console.print(f"\n[bold blue]🔍 Searching Encrypted Repository[/bold blue]\n")
    console.print(f"Keyword: [yellow]{keyword}[/yellow]\n")
    
    # Load encryption key
    key_path = Path('encrypted/aes_key.bin')
    if not key_path.exists():
        console.print("[red]❌ Encryption key not found![/red]")
        console.print("[yellow]Run 'python main.py encrypt' first[/yellow]")
        return
    
    with open(key_path, 'rb') as f:
        key = f.read()
    
    # Create encryptor
    encryptor = FileEncryptor()
    
    # Search
    console.print("🔐 Searching encrypted files...")
    matches = encryptor.search_encrypted(keyword, key)
    
    # Display results
    if matches:
        console.print(f"\n[green]✅ Found {len(matches)} matches:[/green]\n")
        for i, match in enumerate(matches, 1):
            console.print(f"  {i}. 📄 {match['file']}")
    else:
        console.print("\n[yellow]No matches found[/yellow]")
    
    console.print(f"\n[dim]💡 Note: Files were searched while encrypted![/dim]\n")


def demo_multi_keyword_search():
    """Demo searching for multiple keywords."""
    console.print("\n[bold cyan]🎯 Multi-Keyword Search Demo[/bold cyan]\n")
    
    keywords = ["def", "import", "class", "hello"]
    
    for keyword in keywords:
        search_encrypted_repository(keyword)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        keyword = " ".join(sys.argv[1:])
        search_encrypted_repository(keyword)
    else:
        # Demo
        console.print("[yellow]Usage: python encrypted_search.py <keyword>[/yellow]")
        console.print("[yellow]Running demo with sample keywords...[/yellow]\n")
        demo_multi_keyword_search()
