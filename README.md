# PyMigrate

A lightweight PostgreSQL migration library providing version-controlled schema management with integrated performance logging and analytics.

## Features

- 📦 PostgreSQL database support
- 🔄 Version-controlled migrations
- ⬆️ Up/down migration capabilities
- 📊 Migration status tracking
- 🛠️ Schema management tools
- 📈 Performance logging and analytics
- 🚀 Batch SQL execution
- ❌ Detailed failure reporting
- 🎨 Interactive CLI with progress tracking
- 📊 Formatted analytics display

## Installation

```bash
pip install pymigrate
```

## Quick Start

1. Create a new migration:
```bash
pymigrate create add_users_table
```

2. Edit the generated migration file in the `migrations` directory:
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

3. Apply migrations:
```bash
pymigrate up
```

4. Check migration status:
```bash
pymigrate status
```

5. View analytics:
```bash
pymigrate analytics
```

6. Rollback last migration:
```bash
pymigrate down
```

## Environment Variables

Set the following environment variables for database connection:

- `PGHOST` - PostgreSQL host
- `PGPORT` - PostgreSQL port
- `PGDATABASE` - Database name
- `PGUSER` - Database user
- `PGPASSWORD` - Database password

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
