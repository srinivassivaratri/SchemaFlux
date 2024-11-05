import os
import re
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from .connectors import BaseConnector, PostgreSQLConnector, MongoDBConnector
from .version import VersionControl
from .analytics import MigrationAnalytics

class MigrationManager:
    def __init__(self, migrations_dir: str = "migrations", db_type: str = "postgresql"):
        self.migrations_dir = migrations_dir
        self.connector = self._create_connector(db_type)
        self.connector.connect()
        self.version_control = VersionControl(self.connector)
        self.analytics = MigrationAnalytics()
        
    def _create_connector(self, db_type: str) -> BaseConnector:
        """Create appropriate database connector based on type."""
        if db_type.lower() == "postgresql":
            return PostgreSQLConnector()
        elif db_type.lower() == "mongodb":
            return MongoDBConnector()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    def _get_migration_files(self) -> List[str]:
        """Get sorted list of migration files."""
        if not os.path.exists(self.migrations_dir):
            return []
        
        files = [f for f in os.listdir(self.migrations_dir) if f.endswith('.sql') or f.endswith('.js')]
        return sorted(files)

    def _parse_migration_file(self, filename: str) -> Dict[str, str]:
        """Parse migration file content into up and down migrations."""
        path = os.path.join(self.migrations_dir, filename)
        with open(path, 'r') as f:
            content = f.read()

        if filename.endswith('.sql'):
            return self._parse_sql_migration(content)
        elif filename.endswith('.js'):
            return self._parse_js_migration(content)
        
        raise ValueError(f"Unsupported migration file type: {filename}")

    def _parse_sql_migration(self, content: str) -> Dict[str, str]:
        """Parse SQL migration content."""
        up_match = re.search(r'-- UP\n(.*?)(?=-- DOWN|$)', content, re.DOTALL)
        down_match = re.search(r'-- DOWN\n(.*?)$', content, re.DOTALL)
        
        return {
            'up': up_match.group(1).strip() if up_match else '',
            'down': down_match.group(1).strip() if down_match else ''
        }

    def _parse_js_migration(self, content: str) -> Dict[str, str]:
        """Parse JavaScript/MongoDB migration content."""
        up_match = re.search(r'// UP\n(.*?)(?=// DOWN|$)', content, re.DOTALL)
        down_match = re.search(r'// DOWN\n(.*?)$', content, re.DOTALL)
        
        return {
            'up': up_match.group(1).strip() if up_match else '',
            'down': down_match.group(1).strip() if down_match else ''
        }

    def _split_statements(self, sql: str) -> List[str]:
        """Split migration content into individual statements."""
        if isinstance(self.connector, PostgreSQLConnector):
            return [stmt.strip() for stmt in sql.split(';') if stmt.strip()]
        elif isinstance(self.connector, MongoDBConnector):
            return [stmt.strip() for stmt in sql.split('\n') if stmt.strip()]

    def create_migration(self, name: str, db_type: Optional[str] = None) -> str:
        """Create a new migration file."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        ext = '.js' if db_type == 'mongodb' else '.sql'
        filename = f"{timestamp}_{name}{ext}"
        path = os.path.join(self.migrations_dir, filename)
        
        if not os.path.exists(self.migrations_dir):
            os.makedirs(self.migrations_dir)
            
        template = """// UP

// DOWN
""" if ext == '.js' else """-- UP

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
                        total_rows_affected=metrics['operations_count']
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
                total_rows_affected=metrics['operations_count']
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
