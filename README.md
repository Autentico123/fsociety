# FSociety Website

A stylish, interactive FSociety-themed website created by Asero using Python Flask.

## Features

- Dark, hacker-themed UI design
- Interactive terminal animations
- About page with FSociety manifesto
- Join page with recruitment form
- API status endpoint
- Easter egg (try the Konami code!)
- SQLite database for storing form submissions
- Admin dashboard to view all submissions
- CLI tool for database management

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```
   setup_db.bat
   ```
   or manually:
   ```
   python -c "from app import app; from models import db; app.app_context().push(); db.create_all()"
   ```
4. Run the application:
   ```
   python app.py
   ```
   or
   ```
   flask run
   ```

## Database Management

This project includes comprehensive database management utilities:

### Database Management Console

A menu-driven interface for all database operations:

```
db_manager.bat
```

### Database CLI

Command-line tool for managing the database:

```
# Show database statistics
python db_cli.py stats

# Export records to CSV
python db_cli.py export --days 7

# Backup the database
python db_cli.py backup

# Find a recruit by handle
python db_cli.py find_recruit handle_name

# Update a recruit's status
python db_cli.py update_status 1 approved

# Purge old records
python db_cli.py purge --days 30
```

### Backup and Restore

Utility for backing up and restoring the database:

```
# Create a backup
python db_backup.py backup

# List available backups
python db_backup.py list

# Restore a backup
python db_backup.py restore backups/fsociety_backup_20250509_120000.db

# Automated backup with rotation
python db_backup.py auto --max 10
```

### Data Export

Export database tables to CSV files:

```
# Export all tables
python db_export.py

# Export specific table
python db_export.py --table recruit

# Export recent records only
python db_export.py --days 7
```

### Database Maintenance

Optimize and clean up the database:

```
# Full maintenance
python db_maintenance.py full

# Check database size
python db_maintenance.py size

# Optimize database
python db_maintenance.py vacuum

# Purge old records
python db_maintenance.py purge --table recruit --days 30 --status rejected
```

### Database Statistics

Generate detailed reports about the database:

```
# Display statistics
python db_stats.py --display

# Generate report file
python db_stats.py

# Generate JSON format
python db_stats.py --format json
```
python db_cli.py purge --days 30
```

## Technologies Used

- Python 3
- Flask web framework
- HTML5/CSS3
- JavaScript
- Terminal-style UI

## Creator

Created by Asero

## Disclaimer

This is a fictional website themed after the hacker group from the TV series "Mr. Robot". It is created for educational and entertainment purposes only.

## License

MIT License
