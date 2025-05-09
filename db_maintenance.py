#!/usr/bin/env python
# db_maintenance.py - FSociety Database Maintenance Utility
# Created by Asero

import os
import sqlite3
import argparse
import time
from datetime import datetime, timedelta

def vacuum_database(database_path):
    """Optimize the database by running VACUUM"""
    try:
        conn = sqlite3.connect(database_path)
        start_time = time.time()
        print(f"Running VACUUM on {database_path}...")
        
        # Run VACUUM to rebuild the database file
        conn.execute("VACUUM")
        conn.close()
        
        elapsed = time.time() - start_time
        print(f"✓ Database optimization completed in {elapsed:.2f} seconds")
        return True
    
    except sqlite3.Error as e:
        print(f"✗ Database optimization failed: {e}")
        return False

def analyze_database(database_path):
    """Run ANALYZE to update database statistics"""
    try:
        conn = sqlite3.connect(database_path)
        start_time = time.time()
        print(f"Running ANALYZE on {database_path}...")
        
        # Run ANALYZE to update statistics
        conn.execute("ANALYZE")
        conn.close()
        
        elapsed = time.time() - start_time
        print(f"✓ Database analysis completed in {elapsed:.2f} seconds")
        return True
    
    except sqlite3.Error as e:
        print(f"✗ Database analysis failed: {e}")
        return False

def purge_old_records(database_path, table, days, status=None):
    """Purge old records from a specific table"""
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        # Calculate cutoff date
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Build the query
        query = f"DELETE FROM {table} WHERE timestamp < ?"
        params = [cutoff_date]
        
        # Add status condition if provided
        if status:
            query += " AND status = ?"
            params.append(status)
        
        # Execute query
        cursor.execute(query, params)
        deleted_count = cursor.rowcount
        conn.commit()
        
        print(f"✓ Purged {deleted_count} records from '{table}' older than {days} days")
        
        # Run VACUUM to reclaim space if records were deleted
        if deleted_count > 0:
            vacuum_database(database_path)
            
        return deleted_count
    
    except sqlite3.Error as e:
        print(f"✗ Purge operation failed: {e}")
        return 0
    
    finally:
        conn.close()

def check_database_size(database_path):
    """Check the size of the database file"""
    try:
        if os.path.exists(database_path):
            size_bytes = os.path.getsize(database_path)
            size_kb = size_bytes / 1024
            size_mb = size_kb / 1024
            
            print(f"Database file size: {size_bytes:,} bytes ({size_mb:.2f} MB)")
            return size_bytes
        else:
            print(f"Database file not found: {database_path}")
            return None
    
    except Exception as e:
        print(f"Error checking database size: {e}")
        return None

def full_maintenance(database_path):
    """Perform a full database maintenance"""
    print(f"Starting full database maintenance on {database_path}...")
    
    # Check initial size
    print("\nInitial database status:")
    initial_size = check_database_size(database_path)
    
    # Purge old records (example: purge old 'rejected' applications older than 30 days)
    print("\nPurging old records:")
    purge_old_records(database_path, 'recruit', 30, 'rejected')
    
    # Run ANALYZE
    print("\nUpdating database statistics:")
    analyze_database(database_path)
    
    # Run VACUUM
    print("\nOptimizing database:")
    vacuum_database(database_path)
    
    # Check final size
    print("\nFinal database status:")
    final_size = check_database_size(database_path)
    
    # Calculate space saved
    if initial_size and final_size:
        saved = initial_size - final_size
        if saved > 0:
            print(f"\nSpace reclaimed: {saved:,} bytes ({saved/1024/1024:.2f} MB)")
        else:
            print("\nNo space reclaimed during maintenance")
    
    print("\nMaintenance completed successfully")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FSociety Database Maintenance Utility')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Vacuum command
    vacuum_parser = subparsers.add_parser('vacuum', help='Optimize database with VACUUM')
    vacuum_parser.add_argument('--database', default='instance/fsociety.db', help='Database path')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Update database statistics')
    analyze_parser.add_argument('--database', default='instance/fsociety.db', help='Database path')
    
    # Purge command
    purge_parser = subparsers.add_parser('purge', help='Purge old records')
    purge_parser.add_argument('--database', default='instance/fsociety.db', help='Database path')
    purge_parser.add_argument('--table', required=True, help='Table name to purge from')
    purge_parser.add_argument('--days', type=int, required=True, help='Purge records older than N days')
    purge_parser.add_argument('--status', help='Only purge records with this status')
    
    # Check size command
    size_parser = subparsers.add_parser('size', help='Check database file size')
    size_parser.add_argument('--database', default='instance/fsociety.db', help='Database path')
    
    # Full maintenance command
    maintenance_parser = subparsers.add_parser('full', help='Perform full database maintenance')
    maintenance_parser.add_argument('--database', default='instance/fsociety.db', help='Database path')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command == 'vacuum':
        vacuum_database(args.database)
    elif args.command == 'analyze':
        analyze_database(args.database)
    elif args.command == 'purge':
        purge_old_records(args.database, args.table, args.days, args.status)
    elif args.command == 'size':
        check_database_size(args.database)
    elif args.command == 'full':
        full_maintenance(args.database)
    else:
        parser.print_help()
