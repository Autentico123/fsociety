#!/usr/bin/env python
# db_export.py - FSociety Database Export Utility
# Created by Asero

import os
import csv
import argparse
import sqlite3
from datetime import datetime, timedelta

def export_table(database_path, table_name, output_dir='exports', days=None):
    """Export a database table to a CSV file"""
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Format timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(output_dir, f'{table_name}_export_{timestamp}.csv')
    
    # Connect to the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    try:
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Build the query
        query = f"SELECT * FROM {table_name}"
        
        # Add date filter if specified
        if days is not None:
            # Assuming the table has a 'timestamp' column
            cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
            query += f" WHERE timestamp >= '{cutoff_date}'"
        
        # Execute query
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Write to CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)  # Write header
            writer.writerows(rows)    # Write data
        
        print(f"✓ Exported {len(rows)} records from '{table_name}' to {output_path}")
        return output_path
    
    except sqlite3.Error as e:
        print(f"✗ Export failed: {e}")
        return None
    
    finally:
        conn.close()

def export_all_tables(database_path, output_dir='exports', days=None):
    """Export all tables from the database to CSV files"""
    # Connect to the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    try:
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Export each table
        exported_files = []
        for table in tables:
            output_path = export_table(database_path, table, output_dir, days)
            if output_path:
                exported_files.append(output_path)
        
        return exported_files
    
    except sqlite3.Error as e:
        print(f"✗ Error getting tables: {e}")
        return []
    
    finally:
        conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FSociety Database Export Utility')
    parser.add_argument('--database', default='instance/fsociety.db', help='Source database path')
    parser.add_argument('--output-dir', default='exports', help='Output directory for CSV files')
    parser.add_argument('--days', type=int, help='Export records from last N days only')
    parser.add_argument('--table', help='Export specific table only')
    
    args = parser.parse_args()
    
    # Execute export
    if args.table:
        export_table(args.database, args.table, args.output_dir, args.days)
    else:
        export_all_tables(args.database, args.output_dir, args.days)
