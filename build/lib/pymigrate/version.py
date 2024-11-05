class VersionControl:
    def __init__(self, connector):
        self.connector = connector
        self._init_version_table()

    def _init_version_table(self):
        """Initialize version control table if it doesn't exist."""
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

    def get_applied_migrations(self):
        """Get list of applied migrations."""
        sql = "SELECT version, name FROM migration_history WHERE success = TRUE ORDER BY version;"
        return [row for row in self.connector.execute(sql)]

    def record_migration(self, version, name, success=True):
        """Record a migration execution."""
        sql = """
        INSERT INTO migration_history (version, name, success)
        VALUES (%s, %s, %s);
        """
        self.connector.execute(sql, (version, name, success))

    def remove_migration(self, version):
        """Remove a migration record during rollback."""
        sql = "DELETE FROM migration_history WHERE version = %s;"
        self.connector.execute(sql, (version,))
