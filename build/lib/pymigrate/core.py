import os
import re
import time
from datetime import datetime
from typing import List, Dict, Any
from .connector import DatabaseConnector
from .version import VersionControl
from .analytics import MigrationAnalytics

class MigrationManager:
    def __init__(self, migrations_dir: str = "migrations"):
        self.migrations_dir = migrations_dir
        self.connector = DatabaseConnector()
        self.connector.connect()
        self.version_control = VersionControl(self.connector)
        self.analytics = MigrationAnalytics()
        
    def _get_migration_files(self) -> List[str]:
        """Get sorted list of migration files."""
        if not os.path.exists(self.migrations_dir):
            return []
        
        files = [f for f in os.listdir(self.migrations_dir) if f.endswith('.sql')]
        return sorted(files)
        
    def _parse_migration_file(self, filename: str) -> Dict[str, str]:
        """Parse migration file content into up and down migrations."""
        path = os.path.join(self.migrations_dir, filename)
        with open(path, 'r') as f:
            content = f.read()
            
        # Split content into up and down migrations
        up_match = re.search(r'-- UP\n(.*?)(?=-- DOWN|$)', content, re.DOTALL)
        down_match = re.search(r'-- DOWN\n(.*?)$', content, re.DOTALL)
        
        return {
            'up': up_match.group(1).strip() if up_match else '',
            'down': down_match.group(1).strip() if down_match else ''
        }
        
    def _split_statements(self, sql: str) -> List[str]:
        """Split SQL into individual statements for batch execution."""
        # Simple statement splitting - can be enhanced for more complex SQL
        return [stmt.strip() for stmt in sql.split(';') if stmt.strip()]
        
    def create_migration(self, name: str) -> str:
        """Create a new migration file."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{name}.sql"
        path = os.path.join(self.migrations_dir, filename)
        
        if not os.path.exists(self.migrations_dir):
            os.makedirs(self.migrations_dir)
            
        template = """-- UP

-- DOWN
"""
        with open(path, 'w') as f:
            f.write(template)
            
        return filename
        
    def apply_migrations(self) -> None:
        """Apply pending migrations."""
        applied = set(version for version, _ in self.version_control.get_applied_migrations())
        files = self._get_migration_files()
        
        for filename in files:
            version = filename.split('_')[0]
            if version not in applied:
                start_time = time.time()
                self.connector.reset_metrics()
                success = True
                error_msg = None
                
                try:
                    migration = self._parse_migration_file(filename)
                    statements = [(stmt, None) for stmt in self._split_statements(migration['up'])]
                    
                    if statements:
                        self.connector.execute_batch(statements)
                        self.version_control.record_migration(version, filename)
                        print(f"Applied migration: {filename}")
                except Exception as e:
                    success = False
                    error_msg = str(e)
                    self.version_control.record_migration(version, filename, False)
                    raise Exception(f"Failed to apply migration {filename}: {str(e)}")
                finally:
                    end_time = time.time()
                    metrics = self.connector.get_metrics()
                    self.analytics.log_migration(
                        migration_file=filename,
                        start_time=start_time,
                        end_time=end_time,
                        success=success,
                        error=error_msg,
                        query_count=metrics['query_count'],
                        total_rows_affected=metrics['rows_affected']
                    )
                    
    def rollback_migration(self) -> None:
        """Rollback the last migration."""
        applied = self.version_control.get_applied_migrations()
        if not applied:
            print("No migrations to rollback")
            return
            
        last_version, last_name = applied[-1]
        start_time = time.time()
        self.connector.reset_metrics()
        success = True
        error_msg = None
        
        try:
            migration = self._parse_migration_file(last_name)
            if migration['down']:
                statements = [(stmt, None) for stmt in self._split_statements(migration['down'])]
                if statements:
                    self.connector.execute_batch(statements)
                    self.version_control.remove_migration(last_version)
                    print(f"Rolled back migration: {last_name}")
            else:
                raise Exception("No down migration specified")
        except Exception as e:
            success = False
            error_msg = str(e)
            raise Exception(f"Failed to rollback migration {last_name}: {str(e)}")
        finally:
            end_time = time.time()
            metrics = self.connector.get_metrics()
            self.analytics.log_migration(
                migration_file=f"{last_name} (rollback)",
                start_time=start_time,
                end_time=end_time,
                success=success,
                error=error_msg,
                query_count=metrics['query_count'],
                total_rows_affected=metrics['rows_affected']
            )
            
    def show_status(self) -> List[Dict[str, Any]]:
        """Show migration status."""
        applied = set(version for version, _ in self.version_control.get_applied_migrations())
        files = self._get_migration_files()
        
        status = []
        for filename in files:
            version = filename.split('_')[0]
            status.append({
                'file': filename,
                'applied': version in applied
            })
        return status
        
    def get_analytics(self) -> Dict[str, Any]:
        """Get migration analytics and statistics."""
        return self.analytics.get_migration_stats()
