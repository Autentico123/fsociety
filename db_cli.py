#!/usr/bin/env python
# db_cli.py - FSociety Database CLI Tool
# Created by Asero

import click
import os
import sqlite3
import csv
from datetime import datetime
from flask import Flask
from models import db, Recruit, Contact

# Create a minimal Flask app context
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/fsociety.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@click.group()
def cli():
    """FSociety Database Management CLI"""
    pass

@cli.command()
def stats():
    """Show database statistics"""
    with app.app_context():
        recruit_count = Recruit.query.count()
        contact_count = Contact.query.count()
        
        click.echo("=== FSociety Database Statistics ===")
        click.echo(f"Total recruitment applications: {recruit_count}")
        click.echo(f"Total contact messages: {contact_count}")
        
        if recruit_count > 0:
            latest_recruit = Recruit.query.order_by(Recruit.timestamp.desc()).first()
            click.echo(f"Latest recruit: {latest_recruit.handle} at {latest_recruit.timestamp}")
            
        if contact_count > 0:
            latest_contact = Contact.query.order_by(Contact.timestamp.desc()).first()
            click.echo(f"Latest contact: {latest_contact.subject} at {latest_contact.timestamp}")

@cli.command()
@click.option('--days', default=7, help='Export records from the last X days')
@click.option('--output', default='export', help='Output filename prefix')
def export(days, output):
    """Export database records to CSV"""
    now = datetime.utcnow()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    
    with app.app_context():
        # Export recruits
        recruits = Recruit.query.filter(
            Recruit.timestamp > now.replace(day=now.day-days)
        ).all()
        
        if recruits:
            recruit_file = f"{output}_recruits_{timestamp}.csv"
            with open(recruit_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Handle', 'Skills', 'Message', 'Timestamp', 'Status', 'IP Address'])
                
                for recruit in recruits:
                    writer.writerow([
                        recruit.id,
                        recruit.handle,
                        recruit.skills,
                        recruit.message,
                        recruit.timestamp,
                        recruit.status,
                        recruit.ip_address
                    ])
            click.echo(f"Exported {len(recruits)} recruitment records to {recruit_file}")
        else:
            click.echo("No recruitment records to export")
        
        # Export contacts
        contacts = Contact.query.filter(
            Contact.timestamp > now.replace(day=now.day-days)
        ).all()
        
        if contacts:
            contact_file = f"{output}_contacts_{timestamp}.csv"
            with open(contact_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Subject', 'Message', 'Timestamp', 'IP Address'])
                
                for contact in contacts:
                    writer.writerow([
                        contact.id,
                        contact.subject,
                        contact.message,
                        contact.timestamp,
                        contact.ip_address
                    ])
            click.echo(f"Exported {len(contacts)} contact records to {contact_file}")
        else:
            click.echo("No contact records to export")

@cli.command()
@click.confirmation_option(prompt='Are you sure you want to purge old records?')
@click.option('--days', default=30, help='Purge records older than X days')
def purge(days):
    """Purge old records from the database"""
    now = datetime.utcnow()
    cutoff_date = now.replace(day=now.day-days)
    
    with app.app_context():
        # Delete old recruits
        old_recruits = Recruit.query.filter(Recruit.timestamp < cutoff_date).all()
        for recruit in old_recruits:
            db.session.delete(recruit)
        
        # Delete old contacts
        old_contacts = Contact.query.filter(Contact.timestamp < cutoff_date).all()
        for contact in old_contacts:
            db.session.delete(contact)
            
        db.session.commit()
        click.echo(f"Purged {len(old_recruits)} old recruit records")
        click.echo(f"Purged {len(old_contacts)} old contact records")

@cli.command()
def backup():
    """Create a backup of the database"""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_file = f"fsociety_backup_{timestamp}.db"
    
    # Connect to the database
    conn = sqlite3.connect('instance/fsociety.db')
    
    # Create the backup
    backup_conn = sqlite3.connect(backup_file)
    conn.backup(backup_conn)
    
    # Close connections
    backup_conn.close()
    conn.close()
    
    click.echo(f"Database backed up to {backup_file}")

@cli.command()
@click.argument('handle')
def find_recruit(handle):
    """Find a recruit by handle"""
    with app.app_context():
        recruits = Recruit.query.filter(Recruit.handle.like(f"%{handle}%")).all()
        
        if recruits:
            click.echo(f"Found {len(recruits)} matches:")
            for recruit in recruits:
                click.echo(f"ID: {recruit.id}, Handle: {recruit.handle}, Status: {recruit.status}")
                click.echo(f"  Skills: {recruit.skills}")
                click.echo(f"  Joined: {recruit.timestamp}")
                click.echo("---")
        else:
            click.echo(f"No recruits found matching '{handle}'")

@cli.command()
@click.argument('recruit_id', type=int)
@click.argument('status', type=click.Choice(['pending', 'approved', 'rejected']))
def update_status(recruit_id, status):
    """Update a recruit's status"""
    with app.app_context():
        recruit = Recruit.query.get(recruit_id)
        
        if recruit:
            old_status = recruit.status
            recruit.status = status
            db.session.commit()
            click.echo(f"Updated recruit {recruit.handle} status from '{old_status}' to '{status}'")
        else:
            click.echo(f"No recruit found with ID {recruit_id}")

if __name__ == '__main__':
    cli()
