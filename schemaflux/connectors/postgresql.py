import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import Any, List, Tuple
from .base import BaseConnector

class PostgreSQLConnector(BaseConnector):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish PostgreSQL connection using environment variables."""
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
            raise Exception(f"PostgreSQL connection failed: {str(e)}")

    def execute(self, operation: str, params: tuple = None) -> Any:
        """Execute single SQL query with optional parameters."""
        try:
            self.cursor.execute(operation, params)
            self._query_count += 1
            if self.cursor.rowcount >= 0:
                self._operations_count += self.cursor.rowcount
            return self.cursor
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Query execution failed: {str(e)}")

    def execute_batch(self, operations: List[Tuple[str, tuple]]) -> None:
        """Execute multiple SQL statements in a batch."""
        try:
            for operation, params in operations:
                self.cursor.execute(operation, params)
                self._query_count += 1
                if self.cursor.rowcount >= 0:
                    self._operations_count += self.cursor.rowcount
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Batch execution failed: {str(e)}")

    def close(self):
        """Close PostgreSQL connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
