import click
from .core import MigrationManager

@click.group()
def cli():
    """Database migration tool for PostgreSQL."""
    pass

@cli.command()
@click.argument('name')
def create(name):
    """Create a new migration file."""
    manager = MigrationManager()
    filename = manager.create_migration(name)
    click.echo(f"Created migration file: {filename}")

@cli.command()
def up():
    """Apply pending migrations."""
    try:
        manager = MigrationManager()
        manager.apply_migrations()
        click.echo("Migrations completed successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
def down():
    """Rollback the last migration."""
    try:
        manager = MigrationManager()
        manager.rollback_migration()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
def status():
    """Show migration status."""
    try:
        manager = MigrationManager()
        status = manager.show_status()
        
        click.echo("\nMigration Status:")
        click.echo("================")
        for item in status:
            status_str = "✓" if item['applied'] else "✗"
            click.echo(f"{status_str} {item['file']}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    cli()
