from typing import List, Tuple
from .connectors.base import BaseConnector
from .connectors.postgresql import PostgreSQLConnector
from .connectors.mongodb import MongoDBConnector

class VersionControl:
    def __init__(self, connector: BaseConnector):
        self.connector = connector
        self._init_version_table()

    def _init_version_table(self):
        """Initialize version control table/collection."""
        if isinstance(self.connector, PostgreSQLConnector):
            self._init_postgresql_version()
        elif isinstance(self.connector, MongoDBConnector):
            self._init_mongodb_version()

    def _init_postgresql_version(self):
        """Initialize PostgreSQL version table."""
        sql = """
        CREATE TABLE IF NOT EXISTS migration_history (
            id SERIAL PRIMARY KEY,
            version VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            success BOOLEAN DEFAULT TRUE
        );
        """
        self.connector.execute(sql)

    def _init_mongodb_version(self):
        """Initialize MongoDB version collection."""
        op = "create_collection:migration_history:{'validator': {'$jsonSchema': {'bsonType': 'object','required': ['version', 'name', 'applied_at', 'success']}}}"
        try:
            self.connector.execute(op)
        except Exception:
            # Collection might already exist
            pass

    def get_applied_migrations(self) -> List[Tuple[str, str]]:
        """Get list of applied migrations."""
        if isinstance(self.connector, PostgreSQLConnector):
            sql = "SELECT version, name FROM migration_history WHERE success = TRUE ORDER BY version;"
            return [row for row in self.connector.execute(sql)]
        elif isinstance(self.connector, MongoDBConnector):
            op = "find:migration_history:{'filter': {'success': True}, 'sort': [('version', 1)]}"
            result = self.connector.execute(op)
            return [(doc['version'], doc['name']) for doc in result]

    def record_migration(self, version: str, name: str, success: bool = True):
        """Record a migration execution."""
        if isinstance(self.connector, PostgreSQLConnector):
            sql = """
            INSERT INTO migration_history (version, name, success)
            VALUES (%s, %s, %s);
            """
            self.connector.execute(sql, (version, name, success))
        elif isinstance(self.connector, MongoDBConnector):
            op = "insert_one:migration_history:{'document': {'version': '%s', 'name': '%s', 'success': %s, 'applied_at': {'$date': '%s'}}}" % (
                version, name, str(success).lower(), datetime.now().isoformat()
            )
            self.connector.execute(op)

    def remove_migration(self, version: str):
        """Remove a migration record during rollback."""
        if isinstance(self.connector, PostgreSQLConnector):
            sql = "DELETE FROM migration_history WHERE version = %s;"
            self.connector.execute(sql, (version,))
        elif isinstance(self.connector, MongoDBConnector):
            op = "delete_many:migration_history:{'filter': {'version': '%s'}}" % version
            self.connector.execute(op)
