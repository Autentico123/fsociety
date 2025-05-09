#!/usr/bin/env python
# db_backup.py - FSociety Database Backup Utility
# Created by Asero

import os
import sqlite3
import argparse
import time
import shutil
from datetime import datetime

def backup_database(source_path='instance/fsociety.db', backup_dir='backups'):
    """Create a backup of the FSociety SQLite database"""
    # Ensure backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Format timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'fsociety_backup_{timestamp}.db')
    
    # Connect to the source database
    if os.path.exists(source_path):
        try:
            # Create connection to source database
            source_conn = sqlite3.connect(source_path)
            
            # Create backup connection
            backup_conn = sqlite3.connect(backup_path)
            
            # Backup database
            source_conn.backup(backup_conn)
            
            # Close connections
            source_conn.close()
            backup_conn.close()
            
            print(f"✓ Database backup successful: {backup_path}")
            return backup_path
        except sqlite3.Error as e:
            print(f"✗ Backup failed: {e}")
            return None
    else:
        print(f"✗ Source database not found: {source_path}")
        return None

def restore_database(backup_path, target_path='instance/fsociety.db'):
    """Restore a backup to the FSociety SQLite database"""
    if not os.path.exists(backup_path):
        print(f"✗ Backup file not found: {backup_path}")
        return False
    
    # Create backup of current database before restoring
    current_backup = None
    if os.path.exists(target_path):
        current_backup = backup_database(target_path, 'restore_safety')
        
    try:
        # Make sure target directory exists
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # Connect to the backup database
        source_conn = sqlite3.connect(backup_path)
        
        # Connect to target database (create if doesn't exist)
        target_conn = sqlite3.connect(target_path)
        
        # Restore database
        source_conn.backup(target_conn)
        
        # Close connections
        source_conn.close()
        target_conn.close()
        
        print(f"✓ Database successfully restored from: {backup_path}")
        return True
    except sqlite3.Error as e:
        print(f"✗ Restore failed: {e}")
        
        # Try to recover the previous database if restore failed
        if current_backup:
            print("Attempting to recover previous database state...")
            try:
                shutil.copy(current_backup, target_path)
                print("✓ Previous database state recovered")
            except Exception as recovery_error:
                print(f"✗ Recovery failed: {recovery_error}")
                
        return False

def list_backups(backup_dir='backups'):
    """List all available database backups"""
    if not os.path.exists(backup_dir):
        print(f"No backups found (directory '{backup_dir}' doesn't exist)")
        return []
    
    backups = [f for f in os.listdir(backup_dir) if f.startswith('fsociety_backup_') and f.endswith('.db')]
    
    if backups:
        print(f"Available backups in '{backup_dir}':")
        for idx, backup in enumerate(backups, 1):
            # Extract timestamp from filename
            try:
                timestamp_str = backup.replace('fsociety_backup_', '').replace('.db', '')
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                
                # Get file size
                size_bytes = os.path.getsize(os.path.join(backup_dir, backup))
                size_mb = size_bytes / (1024 * 1024)
                
                print(f"  {idx}. {backup} ({timestamp.strftime('%Y-%m-%d %H:%M:%S')}, {size_mb:.2f} MB)")
            except Exception:
                print(f"  {idx}. {backup}")
    else:
        print(f"No backups found in '{backup_dir}'")
    
    return backups

def auto_backup(backup_dir='backups', max_backups=10):
    """Create an automatic backup and maintain only the most recent backups"""
    # Create the backup
    backup_path = backup_database(backup_dir=backup_dir)
    
    if backup_path:
        # List all backups
        all_backups = [os.path.join(backup_dir, f) for f in os.listdir(backup_dir) 
                      if f.startswith('fsociety_backup_') and f.endswith('.db')]
        
        # Sort backups by modification time (oldest first)
        all_backups.sort(key=lambda x: os.path.getmtime(x))
        
        # Remove oldest backups if we have more than max_backups
        while len(all_backups) > max_backups:
            oldest = all_backups.pop(0)
            try:
                os.remove(oldest)
                print(f"Removed old backup: {oldest}")
            except Exception as e:
                print(f"Failed to remove old backup {oldest}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FSociety Database Backup Utility')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create a database backup')
    backup_parser.add_argument('--source', default='instance/fsociety.db', help='Source database path')
    backup_parser.add_argument('--backup-dir', default='backups', help='Backup directory')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore a database backup')
    restore_parser.add_argument('backup', help='Backup file to restore from')
    restore_parser.add_argument('--target', default='instance/fsociety.db', help='Target database path')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available backups')
    list_parser.add_argument('--backup-dir', default='backups', help='Backup directory')
    
    # Auto backup command
    auto_parser = subparsers.add_parser('auto', help='Create an automatic backup and maintain rotation')
    auto_parser.add_argument('--backup-dir', default='backups', help='Backup directory')
    auto_parser.add_argument('--max', type=int, default=10, help='Maximum number of backups to keep')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command == 'backup':
        backup_database(args.source, args.backup_dir)
    elif args.command == 'restore':
        restore_database(args.backup, args.target)
    elif args.command == 'list':
        list_backups(args.backup_dir)
    elif args.command == 'auto':
        auto_backup(args.backup_dir, args.max)
    else:
        parser.print_help()
