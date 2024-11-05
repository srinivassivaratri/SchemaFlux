import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import List, Tuple, Any

class DatabaseConnector:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self._query_count = 0
        self._rows_affected = 0
        
    def connect(self):
        """Establish database connection using environment variables."""
        try:
            self.conn = psycopg2.connect(
                host=os.environ.get('PGHOST'),
                database=os.environ.get('PGDATABASE'),
                user=os.environ.get('PGUSER'),
                password=os.environ.get('PGPASSWORD'),
                port=os.environ.get('PGPORT')
            )
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            raise Exception(f"Database connection failed: {str(e)}")
            
    def execute(self, sql: str, params: tuple = None) -> Any:
        """Execute single SQL query with optional parameters."""
        try:
            self.cursor.execute(sql, params)
            self._query_count += 1
            if self.cursor.rowcount >= 0:  # -1 means no row count available
                self._rows_affected += self.cursor.rowcount
            return self.cursor
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Query execution failed: {str(e)}")
            
    def execute_batch(self, statements: List[Tuple[str, tuple]]) -> None:
        """Execute multiple SQL statements in a batch."""
        try:
            for sql, params in statements:
                self.cursor.execute(sql, params)
                self._query_count += 1
                if self.cursor.rowcount >= 0:
                    self._rows_affected += self.cursor.rowcount
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Batch execution failed: {str(e)}")
            
    def get_metrics(self) -> dict:
        """Get query execution metrics."""
        return {
            'query_count': self._query_count,
            'rows_affected': self._rows_affected
        }
        
    def reset_metrics(self) -> None:
        """Reset query metrics."""
        self._query_count = 0
        self._rows_affected = 0
        
    def close(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
