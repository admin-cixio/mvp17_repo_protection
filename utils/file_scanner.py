"""
File Scanner for Repository
Scans repository and returns list of files to encrypt.
"""

from pathlib import Path
from typing import List, Set
import os


class FileScanner:
    """Scans repository for files to encrypt."""
    
    def __init__(self, root_dir: str = "."):
        """
        Initialize FileScanner.
        
        Args:
            root_dir: Root directory to scan
        """
        self.root_dir = Path(root_dir)
        self.files: List[Path] = []
    
    def scan(self, 
             extensions: List[str] = None,
             max_size_mb: float = 10.0) -> List[Path]:
        """
        Scan directory for files.
        
        Args:
            extensions: List of file extensions to include (e.g., ['.py', '.js'])
                       If None, includes all files
            max_size_mb: Maximum file size in MB to include
            
        Returns:
            List of file paths
        """
        print(f"🔍 Scanning repository: {self.root_dir}")
        
        self.files = []
        max_size_bytes = max_size_mb * 1024 * 1024
        
        for root, dirs, files in os.walk(self.root_dir):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                # Skip hidden files
                if file.startswith('.'):
                    continue
                
                file_path = Path(root) / file
                
                # Check extension
                if extensions and file_path.suffix not in extensions:
                    continue
                
                # Check file size
                try:
                    file_size = file_path.stat().st_size
                    if file_size > max_size_bytes:
                        print(f"  ⚠️  Skipping large file: {file_path} ({file_size / 1024 / 1024:.2f} MB)")
                        continue
                except Exception as e:
                    print(f"  ⚠️  Error checking {file_path}: {e}")
                    continue
                
                self.files.append(file_path)
        
        print(f"✅ Found {len(self.files)} files")
        return self.files
    
    def get_file_stats(self) -> dict:
        """
        Get statistics about scanned files.
        
        Returns:
            Dictionary with file statistics
        """
        if not self.files:
            return {}
        
        total_size = 0
        extensions = {}
        
        for file_path in self.files:
            # Size
            try:
                size = file_path.stat().st_size
                total_size += size
            except:
                continue
            
            # Extension count
            ext = file_path.suffix or 'no_extension'
            extensions[ext] = extensions.get(ext, 0) + 1
        
        return {
            'total_files': len(self.files),
            'total_size_mb': total_size / 1024 / 1024,
            'extensions': extensions
        }
    
    def print_stats(self):
        """Print file statistics."""
        stats = self.get_file_stats()
        
        if not stats:
            print("No files scanned yet")
            return
        
        print("\n📊 Repository Statistics:")
        print(f"   Total Files: {stats['total_files']}")
        print(f"   Total Size: {stats['total_size_mb']:.2f} MB")
        print(f"\n   File Types:")
        
        for ext, count in sorted(stats['extensions'].items(), key=lambda x: x[1], reverse=True):
            print(f"      {ext}: {count}")
    
    def filter_by_extension(self, extensions: List[str]) -> List[Path]:
        """
        Filter files by extension.
        
        Args:
            extensions: List of extensions to include
            
        Returns:
            Filtered list of files
        """
        return [f for f in self.files if f.suffix in extensions]
    
    def filter_by_size(self, max_size_mb: float) -> List[Path]:
        """
        Filter files by size.
        
        Args:
            max_size_mb: Maximum file size in MB
            
        Returns:
            Filtered list of files
        """
        max_bytes = max_size_mb * 1024 * 1024
        filtered = []
        
        for file_path in self.files:
            try:
                if file_path.stat().st_size <= max_bytes:
                    filtered.append(file_path)
            except:
                continue
        
        return filtered


if __name__ == "__main__":
    # Demo usage
    scanner = FileScanner()
    files = scanner.scan(extensions=['.py', '.txt', '.md'])
    scanner.print_stats()
