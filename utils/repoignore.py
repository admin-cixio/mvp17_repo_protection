"""
.repoignore Parser
Similar to .gitignore - parses patterns to exclude files from encryption.
"""

import pathspec
from pathlib import Path
from typing import List, Set


class RepoIgnore:
    """Handles .repoignore file parsing and matching."""
    
    def __init__(self, repoignore_path: str = ".repoignore"):
        """
        Initialize RepoIgnore parser.
        
        Args:
            repoignore_path: Path to .repoignore file
        """
        self.repoignore_path = Path(repoignore_path)
        self.spec = None
        self.patterns: List[str] = []
    
    def load(self) -> bool:
        """
        Load and parse .repoignore file.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        if not self.repoignore_path.exists():
            print(f"⚠️  .repoignore not found at: {self.repoignore_path}")
            print("   Creating default .repoignore...")
            self._create_default()
            return False
        
        with open(self.repoignore_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Parse patterns (skip comments and empty lines)
        self.patterns = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                self.patterns.append(line)
        
        # Create pathspec for matching
        self.spec = pathspec.PathSpec.from_lines('gitwildmatch', self.patterns)
        
        print(f"✅ Loaded {len(self.patterns)} patterns from .repoignore")
        return True
    
    def _create_default(self):
        """Create a default .repoignore file."""
        default_patterns = [
            "# Default .repoignore patterns",
            "",
            "# Keys and secrets",
            "keys/",
            "*.pem",
            "*.key",
            "",
            "# Encrypted files",
            "encrypted/",
            "",
            "# Python cache",
            "__pycache__/",
            "*.pyc",
            "",
            "# Git",
            ".git/",
            ".gitignore",
            "",
            "# This file",
            ".repoignore"
        ]
        
        with open(self.repoignore_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(default_patterns))
        
        print(f"📝 Created default .repoignore at: {self.repoignore_path}")
    
    def is_ignored(self, file_path: Path) -> bool:
        """
        Check if a file should be ignored.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file should be ignored, False otherwise
        """
        if self.spec is None:
            return False
        
        # Convert to relative path string
        try:
            rel_path = str(file_path.relative_to('.'))
        except ValueError:
            rel_path = str(file_path)
        
        # Check if path matches any pattern
        return self.spec.match_file(rel_path)
    
    def filter_files(self, file_list: List[Path]) -> List[Path]:
        """
        Filter file list, removing ignored files.
        
        Args:
            file_list: List of file paths
            
        Returns:
            Filtered list of files
        """
        if self.spec is None:
            self.load()
        
        filtered = []
        ignored_count = 0
        
        for file_path in file_list:
            if self.is_ignored(file_path):
                ignored_count += 1
            else:
                filtered.append(file_path)
        
        print(f"📋 Filtered {len(file_list)} files:")
        print(f"   ✅ Included: {len(filtered)}")
        print(f"   ⛔ Ignored: {ignored_count}")
        
        return filtered
    
    def get_patterns(self) -> List[str]:
        """
        Get list of ignore patterns.
        
        Returns:
            List of patterns
        """
        return self.patterns.copy()
    
    def add_pattern(self, pattern: str):
        """
        Add a new ignore pattern.
        
        Args:
            pattern: Pattern to add
        """
        if pattern not in self.patterns:
            self.patterns.append(pattern)
            
            # Append to file
            with open(self.repoignore_path, 'a', encoding='utf-8') as f:
                f.write(f"\n{pattern}")
            
            # Reload spec
            self.spec = pathspec.PathSpec.from_lines('gitwildmatch', self.patterns)
            print(f"✅ Added pattern: {pattern}")


if __name__ == "__main__":
    # Demo usage
    ri = RepoIgnore()
    ri.load()
    
    # Test some paths
    test_paths = [
        Path("hello_world.py"),
        Path("keys/private_key.pem"),
        Path("encrypted/test.enc"),
        Path(".git/config"),
        Path("main.py")
    ]
    
    print("\n🧪 Testing patterns:")
    for path in test_paths:
        ignored = ri.is_ignored(path)
        status = "⛔ IGNORED" if ignored else "✅ INCLUDED"
        print(f"   {status}: {path}")
