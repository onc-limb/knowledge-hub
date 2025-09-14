"""Progress tracking utilities for the proofreading service.

This module provides progress tracking and reporting functionality.
"""

import time
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from threading import Thread, Event
import sys


@dataclass
class ProgressStage:
    """Represents a progress stage."""
    
    name: str
    description: str
    percentage: float = 0.0
    status: str = "pending"  # pending, running, completed, failed
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    def start(self):
        """Mark stage as started."""
        self.status = "running"
        self.started_at = datetime.now()
    
    def complete(self, percentage: float = 100.0):
        """Mark stage as completed."""
        self.status = "completed"
        self.percentage = percentage
        self.completed_at = datetime.now()
    
    def fail(self, error_message: str):
        """Mark stage as failed."""
        self.status = "failed"
        self.error_message = error_message
        self.completed_at = datetime.now()
    
    def update(self, percentage: float, description: Optional[str] = None):
        """Update progress percentage and description."""
        self.percentage = percentage
        if description:
            self.description = description


class ProgressTracker:
    """Tracks and reports progress for multi-stage operations."""
    
    def __init__(self, stages: Dict[str, str], update_interval: float = 0.5):
        """Initialize progress tracker.
        
        Args:
            stages: Dictionary of stage_id -> stage_description.
            update_interval: How often to update progress display (seconds).
        """
        self.stages = {
            stage_id: ProgressStage(name=stage_id, description=desc)
            for stage_id, desc in stages.items()
        }
        self.update_interval = update_interval
        self.callbacks: list[Callable] = []
        self.started_at = None
        self.completed_at = None
        self._stop_event = Event()
        self._display_thread: Optional[Thread] = None
        self.quiet_mode = False
    
    def add_callback(self, callback: Callable[[str, float, str], None]):
        """Add a progress update callback.
        
        Args:
            callback: Function that receives (stage_id, percentage, description).
        """
        self.callbacks.append(callback)
    
    def start(self, quiet: bool = False):
        """Start progress tracking.
        
        Args:
            quiet: If True, don't display progress bars.
        """
        self.started_at = datetime.now()
        self.quiet_mode = quiet
        
        if not quiet:
            self._start_display_thread()
    
    def _start_display_thread(self):
        """Start background thread for progress display."""
        self._display_thread = Thread(target=self._display_loop, daemon=True)
        self._display_thread.start()
    
    def _display_loop(self):
        """Background loop for updating progress display."""
        while not self._stop_event.is_set():
            if not self.quiet_mode:
                self._update_display()
            time.sleep(self.update_interval)
    
    def _update_display(self):
        """Update console progress display."""
        # Clear previous lines
        for _ in range(len(self.stages) + 2):
            sys.stdout.write("\r\033[K\033[A")
        
        # Print progress bars
        for stage_id, stage in self.stages.items():
            bar = self._create_progress_bar(stage.percentage, stage.status)
            emoji = self._get_status_emoji(stage.status)
            print(f"{emoji} {stage.description:<20} {bar} {stage.percentage:5.1f}%")
        
        # Print overall status
        overall_percentage = self._calculate_overall_percentage()
        elapsed = self._get_elapsed_time()
        print(f"\n全体進捗: {overall_percentage:5.1f}% | 経過時間: {elapsed}")
        
        sys.stdout.flush()
    
    def _create_progress_bar(self, percentage: float, status: str) -> str:
        """Create a visual progress bar."""
        bar_width = 20
        filled = int(bar_width * percentage / 100)
        
        if status == "failed":
            char = "✗"
        elif status == "completed":
            char = "█"
        elif status == "running":
            char = "█"
        else:
            char = "░"
        
        bar = char * filled + "░" * (bar_width - filled)
        return f"[{bar}]"
    
    def _get_status_emoji(self, status: str) -> str:
        """Get emoji for status."""
        emojis = {
            "pending": "⏳",
            "running": "⚡",
            "completed": "✅",
            "failed": "❌"
        }
        return emojis.get(status, "❓")
    
    def _calculate_overall_percentage(self) -> float:
        """Calculate overall progress percentage."""
        if not self.stages:
            return 0.0
        
        total = sum(stage.percentage for stage in self.stages.values())
        return total / len(self.stages)
    
    def _get_elapsed_time(self) -> str:
        """Get formatted elapsed time."""
        if not self.started_at:
            return "0.0s"
        
        elapsed = (datetime.now() - self.started_at).total_seconds()
        
        if elapsed < 60:
            return f"{elapsed:.1f}s"
        else:
            minutes = int(elapsed // 60)
            seconds = elapsed % 60
            return f"{minutes}m {seconds:.1f}s"
    
    def start_stage(self, stage_id: str):
        """Start a specific stage.
        
        Args:
            stage_id: ID of the stage to start.
        """
        if stage_id in self.stages:
            self.stages[stage_id].start()
            self._notify_callbacks(stage_id, 0.0, f"開始: {self.stages[stage_id].description}")
    
    def update_stage(self, stage_id: str, percentage: float, description: Optional[str] = None):
        """Update stage progress.
        
        Args:
            stage_id: ID of the stage to update.
            percentage: Progress percentage (0-100).
            description: Optional updated description.
        """
        if stage_id in self.stages:
            self.stages[stage_id].update(percentage, description)
            desc = description or self.stages[stage_id].description
            self._notify_callbacks(stage_id, percentage, desc)
    
    def complete_stage(self, stage_id: str, description: Optional[str] = None):
        """Mark stage as completed.
        
        Args:
            stage_id: ID of the stage to complete.
            description: Optional completion description.
        """
        if stage_id in self.stages:
            self.stages[stage_id].complete()
            if description:
                self.stages[stage_id].description = description
            self._notify_callbacks(stage_id, 100.0, f"完了: {self.stages[stage_id].description}")
    
    def fail_stage(self, stage_id: str, error_message: str):
        """Mark stage as failed.
        
        Args:
            stage_id: ID of the stage that failed.
            error_message: Error description.
        """
        if stage_id in self.stages:
            self.stages[stage_id].fail(error_message)
            self._notify_callbacks(stage_id, 0.0, f"失敗: {error_message}")
    
    def complete(self):
        """Mark all tracking as completed."""
        self.completed_at = datetime.now()
        self._stop_event.set()
        
        if self._display_thread and self._display_thread.is_alive():
            self._display_thread.join(timeout=1.0)
        
        if not self.quiet_mode:
            self._final_display()
    
    def _final_display(self):
        """Display final progress summary."""
        print("\n" + "="*60)
        print("処理完了サマリー")
        print("="*60)
        
        for stage_id, stage in self.stages.items():
            emoji = self._get_status_emoji(stage.status)
            duration = ""
            if stage.started_at and stage.completed_at:
                duration = f" ({(stage.completed_at - stage.started_at).total_seconds():.1f}s)"
            
            print(f"{emoji} {stage.description:<30} {stage.status.upper()}{duration}")
        
        total_time = self._get_elapsed_time()
        overall_percentage = self._calculate_overall_percentage()
        print(f"\n総合結果: {overall_percentage:.1f}% | 総処理時間: {total_time}")
    
    def _notify_callbacks(self, stage_id: str, percentage: float, description: str):
        """Notify all registered callbacks.
        
        Args:
            stage_id: Stage identifier.
            percentage: Progress percentage.
            description: Progress description.
        """
        for callback in self.callbacks:
            try:
                callback(stage_id, percentage, description)
            except Exception as e:
                # Don't let callback errors break progress tracking
                print(f"Warning: Progress callback error: {e}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get progress summary as dictionary.
        
        Returns:
            Dictionary containing progress summary.
        """
        return {
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "overall_percentage": self._calculate_overall_percentage(),
            "elapsed_time": self._get_elapsed_time(),
            "stages": {
                stage_id: {
                    "description": stage.description,
                    "percentage": stage.percentage,
                    "status": stage.status,
                    "started_at": stage.started_at.isoformat() if stage.started_at else None,
                    "completed_at": stage.completed_at.isoformat() if stage.completed_at else None,
                    "error_message": stage.error_message
                }
                for stage_id, stage in self.stages.items()
            }
        }