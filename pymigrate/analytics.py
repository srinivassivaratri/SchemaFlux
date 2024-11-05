import time
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class MigrationAnalytics:
    def __init__(self, log_dir: str = "migration_logs"):
        self.log_dir = log_dir
        self._ensure_log_dir()
        
    def _ensure_log_dir(self):
        """Ensure the log directory exists."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
    def _get_log_file(self) -> str:
        """Get the log file path for the current day."""
        date_str = datetime.now().strftime('%Y%m%d')
        return os.path.join(self.log_dir, f"migration_log_{date_str}.json")
    
    def log_migration(self, migration_file: str, start_time: float, end_time: float,
                     success: bool, error: str = None, query_count: int = 0,
                     total_rows_affected: int = 0) -> Dict[str, Any]:
        """Log migration execution details."""
        duration = end_time - start_time
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'migration_file': migration_file,
            'duration_seconds': duration,
            'success': success,
            'error': error,
            'query_count': query_count,
            'total_rows_affected': total_rows_affected
        }
        
        log_file = self._get_log_file()
        existing_logs = []
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                try:
                    existing_logs = json.load(f)
                except json.JSONDecodeError:
                    existing_logs = []
                    
        existing_logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(existing_logs, f, indent=2)
            
        return log_entry
    
    def get_migration_stats(self) -> Dict[str, Any]:
        """Get statistics about migrations."""
        all_logs = []
        for filename in os.listdir(self.log_dir):
            if filename.startswith('migration_log_') and filename.endswith('.json'):
                with open(os.path.join(self.log_dir, filename), 'r') as f:
                    try:
                        logs = json.load(f)
                        all_logs.extend(logs)
                    except json.JSONDecodeError:
                        continue
                        
        if not all_logs:
            return {
                'total_migrations': 0,
                'successful_migrations': 0,
                'failed_migrations': 0,
                'average_duration': 0,
                'total_queries': 0,
                'total_rows_affected': 0
            }
            
        successful = [log for log in all_logs if log['success']]
        failed = [log for log in all_logs if not log['success']]
        
        return {
            'total_migrations': len(all_logs),
            'successful_migrations': len(successful),
            'failed_migrations': len(failed),
            'average_duration': sum(log['duration_seconds'] for log in all_logs) / len(all_logs),
            'total_queries': sum(log['query_count'] for log in all_logs),
            'total_rows_affected': sum(log['total_rows_affected'] for log in all_logs)
        }
