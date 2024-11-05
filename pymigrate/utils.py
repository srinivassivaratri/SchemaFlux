import os
import re

def validate_migration_name(name):
    """Validate migration name format."""
    pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, name))

def ensure_migrations_dir(directory):
    """Ensure migrations directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def parse_sql_file(content):
    """Parse SQL file content and extract migrations."""
    up_pattern = r'-- UP\n(.*?)(?=-- DOWN|$)'
    down_pattern = r'-- DOWN\n(.*?)$'
    
    up_match = re.search(up_pattern, content, re.DOTALL)
    down_match = re.search(down_pattern, content, re.DOTALL)
    
    return {
        'up': up_match.group(1).strip() if up_match else '',
        'down': down_match.group(1).strip() if down_match else ''
    }
