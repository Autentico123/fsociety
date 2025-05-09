from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

class Recruit(db.Model):
    """Model for storing FSociety recruitment submissions"""
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    passphrase = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="pending")  # pending, approved, rejected
    
    def __repr__(self):
        return f'<Recruit {self.handle}>'

class Contact(db.Model):
    """Model for storing contact form submissions"""
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    pgp_key = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contact {self.id}: {self.subject}>'
