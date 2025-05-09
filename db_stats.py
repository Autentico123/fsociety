#!/usr/bin/env python
# db_stats.py - FSociety Database Statistics Report
# Created by Asero

import os
import sqlite3
import argparse
from datetime import datetime, timedelta
import json

def get_basic_stats(database_path):
    """Get basic statistics about the database"""
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        # Get table counts
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        table_counts = {}
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            table_counts[table] = count
        
        # Get database file size
        size_bytes = os.path.getsize(database_path)
        size_kb = size_bytes / 1024
        size_mb = size_kb / 1024
        
        # Last modified time
        last_modified = datetime.fromtimestamp(os.path.getmtime(database_path))
        
        basic_stats = {
            "file_path": database_path,
            "file_size_bytes": size_bytes,
            "file_size_mb": size_mb,
            "last_modified": last_modified.strftime('%Y-%m-%d %H:%M:%S'),
            "tables": len(tables),
            "records_by_table": table_counts,
            "total_records": sum(table_counts.values())
        }
        
        return basic_stats
    
    except sqlite3.Error as e:
        print(f"Error getting basic stats: {e}")
        return None
    
    finally:
        if 'conn' in locals():
            conn.close()

def get_detailed_stats(database_path):
    """Get more detailed statistics about records in the database"""
    try:
        conn = sqlite3.connect(database_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()
        
        stats = {}
        
        # Recruits statistics
        try:
            # Total recruits by status
            cursor.execute("SELECT status, COUNT(*) as count FROM recruit GROUP BY status")
            status_counts = {row['status']: row['count'] for row in cursor.fetchall()}
            
            # Recruits per day (last 7 days)
            one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            cursor.execute(f"""
                SELECT date(timestamp) as day, COUNT(*) as count 
                FROM recruit 
                WHERE date(timestamp) >= '{one_week_ago}'
                GROUP BY date(timestamp)
                ORDER BY day
            """)
            daily_counts = {row['day']: row['count'] for row in cursor.fetchall()}
            
            stats['recruits'] = {
                "total": sum(status_counts.values()) if status_counts else 0,
                "by_status": status_counts,
                "daily_last_week": daily_counts
            }
        except sqlite3.Error as e:
            stats['recruits'] = {"error": str(e)}
        
        # Contact messages statistics
        try:
            # Total messages
            cursor.execute("SELECT COUNT(*) as count FROM contact")
            total_messages = cursor.fetchone()['count']
            
            # Messages by domain (from email)
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM contact
                WHERE timestamp >= datetime('now', '-30 days')
            """)
            recent_messages = cursor.fetchone()['count']
            
            stats['contacts'] = {
                "total": total_messages,
                "last_30_days": recent_messages
            }
        except sqlite3.Error as e:
            stats['contacts'] = {"error": str(e)}
        
        return stats
    
    except sqlite3.Error as e:
        print(f"Error getting detailed stats: {e}")
        return None
    
    finally:
        if 'conn' in locals():
            conn.close()

def generate_text_report(database_path):
    """Generate a text-based report of database statistics"""
    basic_stats = get_basic_stats(database_path)
    detailed_stats = get_detailed_stats(database_path)
    
    if not basic_stats:
        return "Failed to get database statistics"
    
    report = []
    report.append("=" * 60)
    report.append(" " * 20 + "FSOCIETY DATABASE REPORT")
    report.append(" " * 15 + f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)
    
    report.append("\n[DATABASE FILE INFORMATION]")
    report.append(f"Path: {basic_stats['file_path']}")
    report.append(f"Size: {basic_stats['file_size_bytes']:,} bytes ({basic_stats['file_size_mb']:.2f} MB)")
    report.append(f"Last Modified: {basic_stats['last_modified']}")
    
    report.append("\n[TABLE SUMMARY]")
    report.append(f"Number of tables: {basic_stats['tables']}")
    report.append(f"Total records: {basic_stats['total_records']:,}")
    
    for table, count in basic_stats['records_by_table'].items():
        report.append(f"  - {table}: {count:,} records")
    
    if detailed_stats and 'recruits' in detailed_stats:
        report.append("\n[RECRUITMENT DATA]")
        recruit_stats = detailed_stats['recruits']
        
        if 'error' not in recruit_stats:
            report.append(f"Total recruits: {recruit_stats['total']:,}")
            
            report.append("\nRecruits by status:")
            for status, count in recruit_stats.get('by_status', {}).items():
                report.append(f"  - {status}: {count:,}")
            
            report.append("\nRecent recruit activity (last 7 days):")
            for day, count in recruit_stats.get('daily_last_week', {}).items():
                report.append(f"  - {day}: {count:,} new recruits")
    
    if detailed_stats and 'contacts' in detailed_stats:
        report.append("\n[CONTACT DATA]")
        contact_stats = detailed_stats['contacts']
        
        if 'error' not in contact_stats:
            report.append(f"Total contact messages: {contact_stats['total']:,}")
            report.append(f"Messages in last 30 days: {contact_stats['last_30_days']:,}")
    
    report.append("\n" + "=" * 60)
    report.append(" " * 20 + "END OF REPORT")
    report.append("=" * 60)
    
    return "\n".join(report)

def save_report(report, output_format='txt', output_dir='reports'):
    """Save the report to a file"""
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Format timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if output_format == 'json':
        # For JSON format, report should be a dictionary
        output_path = os.path.join(output_dir, f'fsociety_db_report_{timestamp}.json')
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
    else:
        # For text format, report should be a string
        output_path = os.path.join(output_dir, f'fsociety_db_report_{timestamp}.txt')
        with open(output_path, 'w') as f:
            f.write(report)
    
    print(f"Report saved to {output_path}")
    return output_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FSociety Database Statistics Report')
    parser.add_argument('--database', default='instance/fsociety.db', help='Database path')
    parser.add_argument('--format', choices=['txt', 'json'], default='txt', help='Output format')
    parser.add_argument('--output-dir', default='reports', help='Output directory for reports')
    parser.add_argument('--display', action='store_true', help='Display report on screen')
    
    args = parser.parse_args()
    
    if args.format == 'json':
        basic_stats = get_basic_stats(args.database)
        detailed_stats = get_detailed_stats(args.database)
        report = {
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "basic_stats": basic_stats,
            "detailed_stats": detailed_stats
        }
        
        if args.display:
            print(json.dumps(report, indent=2))
        
        save_report(report, output_format='json', output_dir=args.output_dir)
    else:
        report = generate_text_report(args.database)
        
        if args.display:
            print(report)
        
        save_report(report, output_format='txt', output_dir=args.output_dir)
