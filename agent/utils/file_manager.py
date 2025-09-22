"""
ファイル管理ユーティリティモジュール

このモジュールはファイルの読み書きに関する共通機能を提供します。
"""

from pathlib import Path
from typing import List, Optional


class FileManager:
    """
    ファイル操作を管理するクラス
    
    Markdownファイルの読み込み、ディレクトリ操作などのファイル関連操作を提供します。
    """
    
    def __init__(self, base_directory: Optional[Path] = None):
        """
        FileManagerクラスのコンストラクタ
        
        Args:
            base_directory (Optional[Path]): ベースディレクトリのパス。指定しない場合は相対パスで操作
        """
        self.base_directory = base_directory if base_directory else None
    
    def read_markdown_file(self, file_path: str) -> str:
        """
        指定されたパスからMarkdownファイルを読み込み、内容を文字列として返す
        
        Args:
            file_path (str): 読み込むMarkdownファイルのパス
            
        Returns:
            str: ファイルの内容
            
        Raises:
            FileNotFoundError: ファイルが存在しない場合
            IOError: ファイルの読み込みに失敗した場合
            ValueError: ファイルがMarkdownファイルでない場合
        """
        # ベースディレクトリが設定されている場合は相対パスとして解決
        if self.base_directory and not Path(file_path).is_absolute():
            path = (self.base_directory / file_path).resolve()
        else:
            path = Path(file_path).resolve()
        
        # ファイルの存在確認
        if not path.exists():
            raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
        
        # ファイルかどうかの確認
        if not path.is_file():
            raise ValueError(f"指定されたパスはファイルではありません: {file_path}")
        
        # Markdownファイルかどうかの確認（拡張子チェック）
        if path.suffix.lower() not in ['.md', '.markdown']:
            raise ValueError(f"Markdownファイルではありません: {file_path}")
        
        try:
            # UTF-8エンコーディングでファイルを読み込み
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except IOError as e:
            raise IOError(f"ファイルの読み込みに失敗しました: {file_path}") from e
    
    def get_markdown_files_in_directory(self, directory_path: str) -> List[str]:
        """
        指定されたディレクトリ内のMarkdownファイルのパスを取得する
        
        Args:
            directory_path (str): 検索するディレクトリのパス
            
        Returns:
            List[str]: Markdownファイルのパスのリスト
            
        Raises:
            FileNotFoundError: ディレクトリが存在しない場合
            ValueError: 指定されたパスがディレクトリでない場合
        """
        # ベースディレクトリが設定されている場合は相対パスとして解決
        if self.base_directory and not Path(directory_path).is_absolute():
            path = (self.base_directory / directory_path).resolve()
        else:
            path = Path(directory_path).resolve()
        
        if not path.exists():
            raise FileNotFoundError(f"ディレクトリが見つかりません: {directory_path}")
        
        if not path.is_dir():
            raise ValueError(f"指定されたパスはディレクトリではありません: {directory_path}")
        
        markdown_files = []
        
        # .mdファイルを検索
        for file_path in path.rglob("*.md"):
            if file_path.is_file():
                markdown_files.append(str(file_path))
        
        # .markdownファイルも検索
        for file_path in path.rglob("*.markdown"):
            if file_path.is_file():
                markdown_files.append(str(file_path))
        
        return sorted(markdown_files)
    
    def file_exists(self, file_path: str) -> bool:
        """
        ファイルが存在するかどうかを確認する
        
        Args:
            file_path (str): 確認するファイルのパス
            
        Returns:
            bool: ファイルが存在する場合True、そうでなければFalse
        """
        # ベースディレクトリが設定されている場合は相対パスとして解決
        if self.base_directory and not Path(file_path).is_absolute():
            path = (self.base_directory / file_path).resolve()
        else:
            path = Path(file_path).resolve()
        
        return path.exists() and path.is_file()
    
    def get_file_info(self, file_path: str) -> dict:
        """
        ファイルの情報を取得する
        
        Args:
            file_path (str): 情報を取得するファイルのパス
            
        Returns:
            dict: ファイル情報（パス、サイズ、更新日時など）
            
        Raises:
            FileNotFoundError: ファイルが存在しない場合
        """
        # ベースディレクトリが設定されている場合は相対パスとして解決
        if self.base_directory and not Path(file_path).is_absolute():
            path = (self.base_directory / file_path).resolve()
        else:
            path = Path(file_path).resolve()
        
        if not path.exists():
            raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
        
        stat = path.stat()
        
        return {
            'path': str(path),
            'name': path.name,
            'size': stat.st_size,
            'modified_time': stat.st_mtime,
            'is_file': path.is_file(),
            'is_directory': path.is_dir(),
            'suffix': path.suffix
        }
