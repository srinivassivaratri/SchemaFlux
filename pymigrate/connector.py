import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DatabaseConnector:
    def __init__(self):
        self.conn = None
        self.cursor = None

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

    def execute(self, sql, params=None):
        """Execute SQL query with optional parameters."""
        try:
            self.cursor.execute(sql, params)
            return self.cursor
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Query execution failed: {str(e)}")

    def close(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
