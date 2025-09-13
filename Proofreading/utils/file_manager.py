"""
File utilities for reading and processing articles
"""
import os
import markdown
from pathlib import Path
from typing import List, Dict

class FileManager:
    """Manages file operations for article processing"""
    
    def __init__(self, repository_root: str = None):
        if repository_root is None:
            # Find the repository root (where .git directory exists)
            current_path = Path(__file__).parent
            while current_path.parent != current_path:
                if (current_path / '.git').exists():
                    self.repository_root = current_path
                    break
                current_path = current_path.parent
            else:
                self.repository_root = Path.cwd()
        else:
            self.repository_root = Path(repository_root)
    
    def read_file(self, file_path: str) -> str:
        """Read content from a file"""
        full_path = self.repository_root / file_path
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise FileNotFoundError(f"Could not read file {file_path}: {str(e)}")
    
    def find_markdown_files(self, search_pattern: str = None) -> List[str]:
        """Find markdown files in the repository"""
        markdown_files = []
        for root, dirs, files in os.walk(self.repository_root):
            # Skip .git and other hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.endswith('.md'):
                    relative_path = os.path.relpath(
                        os.path.join(root, file), 
                        self.repository_root
                    )
                    if search_pattern is None or search_pattern in relative_path:
                        markdown_files.append(relative_path)
        
        return markdown_files
    
    def parse_markdown(self, content: str) -> Dict[str, str]:
        """Parse markdown content and extract metadata"""
        lines = content.split('\n')
        
        # Extract title (first heading)
        title = "Untitled"
        for line in lines:
            if line.startswith('#'):
                title = line.lstrip('#').strip()
                break
        
        # Convert to HTML for analysis
        html_content = markdown.markdown(content)
        
        return {
            'title': title,
            'raw_content': content,
            'html_content': html_content,
            'line_count': len(lines),
            'word_count': len(content.split())
        }