"""
Configuration Watcher - Watch config files for changes and auto-reload
"""

import os
import time
import threading
from pathlib import Path
from typing import Callable, Optional


class ConfigWatcher:
    """Watch configuration file for changes"""
    
    def __init__(self, file_path: str, callback: Callable[[], None], 
                 interval: float = 1.0):
        self.file_path = Path(file_path)
        self.callback = callback
        self.interval = interval
        self.last_modified: Optional[float] = None
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        
        # Get initial modification time
        self._update_last_modified()
    
    def _update_last_modified(self) -> bool:
        """Update last modified time, return True if file exists"""
        try:
            stat = self.file_path.stat()
            self.last_modified = stat.st_mtime
            return True
        except (OSError, FileNotFoundError):
            return False
    
    def _check_for_changes(self) -> bool:
        """Check if file has been modified"""
        try:
            stat = self.file_path.stat()
            current_modified = stat.st_mtime
            
            if self.last_modified is None:
                self.last_modified = current_modified
                return False
            
            if current_modified != self.last_modified:
                self.last_modified = current_modified
                return True
            
            return False
        
        except (OSError, FileNotFoundError):
            return False
    
    def _watch_loop(self) -> None:
        """Main watch loop"""
        while self.is_running:
            if self._check_for_changes():
                try:
                    self.callback()
                except Exception as e:
                    print(f"\n⚠️  Error during config reload: {e}")
            
            time.sleep(self.interval)
    
    def start(self) -> None:
        """Start watching for changes"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._watch_loop)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self) -> None:
        """Stop watching for changes"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=self.interval + 0.5)
