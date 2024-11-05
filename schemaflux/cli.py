import click
from .core import MigrationManager

ASCII_BANNER = """
╔═══╗             ╔╗        ╔═══╗      ╔═══╗ ╔╗  
║╔═╗║             ║║        ║╔═╗║      ║╔═╗║ ║║  
║╚═╝║╔╗╔╗╔╗╔═╗    ║║ ╔══╗╔═╗║║ ╚╝╔══╗ ║║ ║║╔╝║  
║╔══╝║╚╝║╚╬╣╔╗╔╗  ║║ ║╔╗║║╔╝║║╔═╗║══╣ ║╚═╝║╚╗║  
║║   ║║║║║║║║║║  ║╚╗║╚╝║║║ ║╚╩═║╠══║ ║╔═╗║ ║║  
╚╝   ╚╩╩╝╚╝╚╝╚╝  ╚═╝╚══╝╚╝ ╚═══╝╚══╝ ╚╝ ╚╝ ╚╝  
PostgreSQL Migration Manager - Version 1.0.0
"""

def print_banner():
    """Print the ASCII art banner with styling."""
    click.echo(click.style(ASCII_BANNER, fg='blue', bold=True))

@click.group()
def cli():
    """Database migration tool for PostgreSQL."""
    print_banner()

@cli.command()
@click.argument('name')
def create(name):
    """Create a new migration file."""
    manager = MigrationManager()
    with click.progressbar(length=1, label='Creating migration file') as bar:
        filename = manager.create_migration(name)
        bar.update(1)
    click.echo(click.style(f"✨ Created migration file: ", fg='green') + 
               click.style(filename, fg='bright_white', bold=True))

@cli.command()
def up():
    """Apply pending migrations."""
    try:
        manager = MigrationManager()
        with click.progressbar(length=1, label='Applying migrations') as bar:
            manager.apply_migrations()
            bar.update(1)
        click.echo(click.style("✅ Migrations completed successfully", fg='green', bold=True))
    except Exception as e:
        click.echo(click.style(f"❌ Error: {str(e)}", fg='red', bold=True), err=True)

@cli.command()
def down():
    """Rollback the last migration."""
    try:
        manager = MigrationManager()
        with click.progressbar(length=1, label='Rolling back migration') as bar:
            manager.rollback_migration()
            bar.update(1)
        click.echo(click.style("✅ Rollback completed successfully", fg='green', bold=True))
    except Exception as e:
        click.echo(click.style(f"❌ Error: {str(e)}", fg='red', bold=True), err=True)

@cli.command()
def status():
    """Show migration status."""
    try:
        manager = MigrationManager()
        status = manager.show_status()
        
        click.echo("\n" + click.style("📊 Migration Status", fg='blue', bold=True))
        click.echo(click.style("═" * 50, fg='blue'))
        
        if not status:
            click.echo(click.style("No migrations found", fg='yellow', italic=True))
        else:
            for item in status:
                if item['applied']:
                    status_icon = click.style("✓", fg='green', bold=True)
                    file_style = click.style(item['file'], fg='bright_white')
                else:
                    status_icon = click.style("✗", fg='red', bold=True)
                    file_style = click.style(item['file'], fg='yellow')
                click.echo(f"{status_icon} {file_style}")
    except Exception as e:
        click.echo(click.style(f"❌ Error: {str(e)}", fg='red', bold=True), err=True)

@cli.command()
def analytics():
    """Show migration analytics and performance statistics."""
    try:
        manager = MigrationManager()
        stats = manager.get_analytics()
        
        click.echo("\n" + click.style("📈 Migration Analytics", fg='blue', bold=True))
        click.echo(click.style("═" * 50, fg='blue'))
        
        # Format statistics with colors and alignment
        metrics = [
            ("🔢 Total Migrations", stats['total_migrations'], 'bright_white'),
            ("✅ Successful", stats['successful_migrations'], 'green'),
            ("❌ Failed", stats['failed_migrations'], 'red'),
            ("⏱️  Average Duration", f"{stats['average_duration']:.2f} seconds", 'cyan'),
            ("📝 Total Queries", stats['total_queries'], 'yellow'),
            ("📊 Total Rows Affected", stats['total_rows_affected'], 'magenta')
        ]
        
        # Calculate padding for alignment
        max_label_length = max(len(label) for label, _, _ in metrics)
        
        for label, value, color in metrics:
            padding = " " * (max_label_length - len(label))
            click.echo(f"{label}{padding}: {click.style(str(value), fg=color, bold=True)}")
            
    except Exception as e:
        click.echo(click.style(f"❌ Error: {str(e)}", fg='red', bold=True), err=True)

if __name__ == '__main__':
    cli()
