"""File management utilities for the proofreading service.

This module handles file operations including reading, writing, and validation.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import chardet

from .models import MarkdownFile, IntegratedReport


class FileManager:
    """Manages file operations for the proofreading service."""
    
    def __init__(self, base_output_dir: str = "reports"):
        """Initialize file manager.
        
        Args:
            base_output_dir: Base directory for output files.
        """
        self.base_output_dir = Path(base_output_dir)
        self.base_output_dir.mkdir(exist_ok=True)
    
    def read_markdown_file(self, file_path: str) -> MarkdownFile:
        """Read and validate a markdown file.
        
        Args:
            file_path: Path to the markdown file.
            
        Returns:
            MarkdownFile object with content and metadata.
            
        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If file is invalid (too large, empty, etc.).
            UnicodeDecodeError: If file encoding is unsupported.
        """
        path_obj = Path(file_path)
        
        # Check if file exists
        if not path_obj.exists():
            raise FileNotFoundError(f"File not found: {path_obj}")
        
        # Check file size (10MB limit)
        file_size = path_obj.stat().st_size
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise ValueError(f"File size ({file_size} bytes) exceeds 10MB limit")
        
        # Detect encoding
        try:
            with open(path_obj, 'rb') as f:
                raw_data = f.read()
            
            detected = chardet.detect(raw_data)
            encoding = detected['encoding'] or 'utf-8'
            
            # Read file content
            content = raw_data.decode(encoding)
            
        except UnicodeDecodeError as e:
            raise ValueError(f"Cannot decode file {path_obj}: {e}")
        
        return MarkdownFile(
            file_path=str(path_obj.absolute()),
            content=content,
            size_bytes=file_size,
            encoding=encoding
        )
    
    def save_report(self, report: IntegratedReport, output_format: str = "markdown", 
                   output_dir: Optional[str] = None) -> str:
        """Save integrated report to file.
        
        Args:
            report: IntegratedReport object to save.
            output_format: Format to save (markdown, json, html).
            output_dir: Custom output directory (optional).
            
        Returns:
            Path to the saved report file.
            
        Raises:
            ValueError: If output format is not supported.
        """
        if output_format not in ["markdown", "json", "html"]:
            raise ValueError(f"Unsupported output format: {output_format}")
        
        # Determine output directory
        if output_dir:
            output_path = Path(output_dir)
        else:
            output_path = self.base_output_dir
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        if report.original_file:
            base_name = Path(report.original_file.file_path).stem
        else:
            base_name = "report"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{base_name}_{timestamp}_proofreading_report.{output_format}"
        file_path = output_path / filename
        
        # Save based on format
        if output_format == "markdown":
            content = self._generate_markdown_report(report)
        elif output_format == "json":
            content = self._generate_json_report(report)
        elif output_format == "html":
            content = self._generate_html_report(report)
        
        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update report with file path
        report.file_path = str(file_path.absolute())
        
        return str(file_path.absolute())
    
    def _generate_markdown_report(self, report: IntegratedReport) -> str:
        """Generate markdown format report."""
        content = []
        
        # Header
        content.append("# 統合校正レポート")
        content.append("")
        content.append(f"**レポートID**: {report.report_id}")
        content.append(f"**生成日時**: {report.generated_at.strftime('%Y年%m月%d日 %H:%M:%S')}")
        content.append(f"**総合評価**: {report.overall_score:.1%}")
        content.append("")
        
        # Original file info
        if report.original_file:
            content.append("## 対象ファイル")
            content.append(f"- **ファイルパス**: {report.original_file.file_path}")
            content.append(f"- **ファイルサイズ**: {report.original_file.size_bytes:,} bytes")
            content.append(f"- **文字エンコーディング**: {report.original_file.encoding}")
            content.append("")
        
        # Executive summary
        if report.executive_summary:
            content.append("## 要約")
            content.append(report.executive_summary)
            content.append("")
        
        # Evidence results
        if report.evidence_result:
            content.append("## エビデンス調査結果")
            ev = report.evidence_result
            content.append(f"- **信頼度スコア**: {ev.confidence_score:.1%}")
            content.append(f"- **処理時間**: {ev.processing_time:.1f}秒")
            
            if ev.verified_facts:
                content.append("### 検証済み事実")
                for fact in ev.verified_facts:
                    content.append(f"- {fact.claim} (信頼度: {fact.confidence:.1%})")
            
            if ev.questionable_claims:
                content.append("### 疑問のある主張")
                for claim in ev.questionable_claims:
                    content.append(f"- {claim.claim} ({claim.severity})")
            
            content.append("")
        
        # Proofreading results
        if report.proofreading_result:
            content.append("## 文章校正結果")
            pr = report.proofreading_result
            content.append(f"- **可読性スコア**: {pr.readability_score:.1%}")
            content.append(f"- **処理時間**: {pr.processing_time:.1f}秒")
            
            if pr.grammar_fixes:
                content.append("### 文法修正")
                for fix in pr.grammar_fixes:
                    content.append(f"- 行{fix.line_number}: {fix.original} → {fix.corrected}")
            
            content.append("")
        
        # Priority actions
        if report.priority_actions:
            content.append("## 優先対応事項")
            for i, action in enumerate(report.priority_actions, 1):
                content.append(f"{i}. **{action.action}** ({action.category}, 優先度{action.priority}, 工数{action.effort})")
            content.append("")
        
        return "\n".join(content)
    
    def _generate_json_report(self, report: IntegratedReport) -> str:
        """Generate JSON format report."""
        data = {
            "report_id": report.report_id,
            "generated_at": report.generated_at.isoformat(),
            "overall_score": report.overall_score,
            "executive_summary": report.executive_summary,
            "file_path": report.file_path
        }
        
        # Original file
        if report.original_file:
            data["original_file"] = {
                "file_path": report.original_file.file_path,
                "size_bytes": report.original_file.size_bytes,
                "encoding": report.original_file.encoding,
                "content": report.original_file.content
            }
        
        # Evidence result
        if report.evidence_result:
            ev = report.evidence_result
            data["evidence_result"] = {
                "agent_id": ev.agent_id,
                "confidence_score": ev.confidence_score,
                "processing_time": ev.processing_time,
                "verified_facts": [
                    {
                        "claim": f.claim,
                        "evidence": f.evidence,
                        "source": f.source,
                        "confidence": f.confidence
                    } for f in ev.verified_facts
                ],
                "questionable_claims": [
                    {
                        "claim": c.claim,
                        "reason": c.reason,
                        "severity": c.severity
                    } for c in ev.questionable_claims
                ],
                "error_message": ev.error_message
            }
        
        # Proofreading result
        if report.proofreading_result:
            pr = report.proofreading_result
            data["proofreading_result"] = {
                "agent_id": pr.agent_id,
                "readability_score": pr.readability_score,
                "processing_time": pr.processing_time,
                "grammar_fixes": [
                    {
                        "line_number": f.line_number,
                        "original": f.original,
                        "corrected": f.corrected,
                        "rule": f.rule
                    } for f in pr.grammar_fixes
                ],
                "error_message": pr.error_message
            }
        
        # Priority actions
        data["priority_actions"] = [
            {
                "action": a.action,
                "category": a.category,
                "priority": a.priority,
                "effort": a.effort
            } for a in report.priority_actions
        ]
        
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def _generate_html_report(self, report: IntegratedReport) -> str:
        """Generate HTML format report."""
        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>統合校正レポート - {report.report_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
        .score {{ font-size: 24px; font-weight: bold; color: #333; }}
        .section {{ margin: 20px 0; }}
        .priority-high {{ color: #d32f2f; }}
        .priority-medium {{ color: #f57c00; }}
        .priority-low {{ color: #388e3c; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>統合校正レポート</h1>
        <p><strong>レポートID:</strong> {report.report_id}</p>
        <p><strong>生成日時:</strong> {report.generated_at.strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        <p class="score"><strong>総合評価:</strong> {report.overall_score:.1%}</p>
    </div>
"""
        
        if report.executive_summary:
            html += f"""
    <div class="section">
        <h2>要約</h2>
        <p>{report.executive_summary}</p>
    </div>
"""
        
        if report.priority_actions:
            html += """
    <div class="section">
        <h2>優先対応事項</h2>
        <table>
            <tr><th>アクション</th><th>カテゴリ</th><th>優先度</th><th>工数</th></tr>
"""
            for action in report.priority_actions:
                priority_class = f"priority-{action.effort}"
                html += f"""
            <tr class="{priority_class}">
                <td>{action.action}</td>
                <td>{action.category}</td>
                <td>{action.priority}</td>
                <td>{action.effort}</td>
            </tr>
"""
            html += """
        </table>
    </div>
"""
        
        html += """
</body>
</html>
"""
        return html
    
    def create_config_example(self, output_path: str):
        """Create an example configuration file.
        
        Args:
            output_path: Path to save the example config file.
        """
        from ..config.agent_config import ConfigManager
        
        config_manager = ConfigManager()
        example_config = config_manager.get_example_config()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(example_config)
    
    def __init__(self, repository_root: str | None = None):
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
    
    def find_markdown_files(self, search_pattern: str | None = None) -> List[str]:
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
    
    def parse_markdown(self, content: str) -> Dict[str, str | int]:
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