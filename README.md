# SchemaFlux 🔄

A powerful PostgreSQL migration tool that makes database schema management a breeze. Track changes, monitor performance, and deploy with confidence.

## Why SchemaFlux?

Managing database schema changes in production is hard. SchemaFlux solves this by providing:
- Version-controlled migrations with automatic rollbacks
- Real-time performance analytics
- Simple CLI interface
- Detailed error reporting

## Quick Start

1. Install:
```bash
pip install schemaflux
```

2. Configure:
```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=your_database
export PGUSER=your_username
export PGPASSWORD=your_password
```

3. Create a migration:
```bash
schemaflux create add_users_table
```

4. Apply it:
```bash
schemaflux up
```

## Usage

### CLI Commands

```bash
schemaflux create <name>  # Create migration
schemaflux up            # Apply migrations
schemaflux down          # Rollback
schemaflux status        # Check status
schemaflux analytics     # View metrics
```

### Python API

```python
from schemaflux import MigrationManager

manager = MigrationManager()
manager.create_migration("add_users_table")
manager.apply_migrations()
```

### Migration Format

```sql
-- UP
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL
);

-- DOWN
DROP TABLE IF EXISTS users;
```

## Contributing

1. Fork it
2. Create your branch (`git checkout -b feature/cool-thing`)
3. Commit changes (`git commit -am 'Added cool thing'`)
4. Push (`git push origin feature/cool-thing`)
5. Open a PR

## License

MIT © SchemaFlux Team

---

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://pypi.org/project/schemaflux/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
