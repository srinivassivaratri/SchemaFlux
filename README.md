# PyMigrate

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://pypi.org/project/pymigrate/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A powerful, lightweight PostgreSQL migration library providing version-controlled schema management with integrated performance logging and analytics. PyMigrate helps you manage database changes with confidence through automated migrations, rollbacks, and comprehensive performance tracking.

## Features

- 📦 **PostgreSQL Support**: Robust support for PostgreSQL databases
- 🔄 **Version Control**: Track and manage database schema versions
- ⬆️ **Bidirectional Migrations**: Support for both up and down migrations
- 📊 **Migration Analytics**: Built-in performance logging and statistics
- 🚀 **Batch Operations**: Efficient batch SQL execution capabilities
- 🎯 **Status Tracking**: Real-time migration status monitoring
- 🔍 **Failure Reporting**: Detailed error tracking and reporting
- 🎨 **Interactive CLI**: Beautiful command-line interface with progress tracking
- 📈 **Performance Metrics**: Track execution time, queries, and affected rows

## Installation

Install PyMigrate using pip:

```bash
pip install pymigrate
```

## Quick Start

### 1. Set Environment Variables

Configure your PostgreSQL connection:

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=your_database
export PGUSER=your_username
export PGPASSWORD=your_password
```

### 2. Create a Migration

Create a new migration file:

```bash
pymigrate create add_users_table
```

This creates a timestamped SQL migration file in the `migrations` directory:

```sql
-- UP
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DOWN
DROP TABLE IF EXISTS users;
```

### 3. Apply Migrations

Run pending migrations:

```bash
pymigrate up
```

### 4. Check Status

View migration status:

```bash
pymigrate status
```

Example output:
```
📊 Migration Status
══════════════════════════════════════════════════
✓ 20241105063812_initial_schema.sql
✗ 20241105070259_add_posts_table.sql
```

### 5. View Analytics

Check migration performance metrics:

```bash
pymigrate analytics
```

Example output:
```
📈 Migration Analytics
══════════════════════════════════════════════════
🔢 Total Migrations   : 12
✅ Successful         : 12
❌ Failed             : 0
⏱️  Average Duration : 0.13 seconds
📝 Total Queries      : 6
📊 Total Rows Affected: 3
```

### 6. Rollback

Rollback the last migration:

```bash
pymigrate down
```

## API Reference

### CLI Commands

| Command | Description |
|---------|-------------|
| `pymigrate create <name>` | Create a new migration file |
| `pymigrate up` | Apply pending migrations |
| `pymigrate down` | Rollback last migration |
| `pymigrate status` | Show migration status |
| `pymigrate analytics` | Display performance metrics |

### Python API

```python
from pymigrate import MigrationManager

# Initialize manager
manager = MigrationManager()

# Create migration
manager.create_migration("add_users_table")

# Apply migrations
manager.apply_migrations()

# Check status
status = manager.show_status()

# Get analytics
metrics = manager.get_analytics()

# Rollback
manager.rollback_migration()
```

## Configuration

PyMigrate uses environment variables for configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `PGHOST` | PostgreSQL host | localhost |
| `PGPORT` | PostgreSQL port | 5432 |
| `PGDATABASE` | Database name | None |
| `PGUSER` | Database user | None |
| `PGPASSWORD` | Database password | None |

## Migration File Format

Migration files support both UP and DOWN migrations:

```sql
-- UP
CREATE TABLE example (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- DOWN
DROP TABLE IF EXISTS example;
```

## Error Handling

PyMigrate provides detailed error reporting:
- Migration failures are logged with timestamps
- Rollback operations are automatically attempted on failure
- Detailed error messages help identify issues quickly

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your PR includes:
- Clear description of changes
- Updated tests if applicable
- Documentation updates

## Best Practices

1. Always include DOWN migrations for rollback capability
2. Use meaningful migration names
3. Keep migrations atomic and focused
4. Test migrations in development before production
5. Review analytics to optimize performance

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- PostgreSQL community for the amazing database
- Click library for the beautiful CLI interface
- All contributors who have helped shape this project

---

Built with ❤️ by the PyMigrate Team
