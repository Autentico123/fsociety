from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import os
from models import db, Recruit, Contact
import sqlite3

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'fsociety_secret_key_by_asero'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fsociety.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Creator attribution
CREATOR = "Asero"

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', creator=CREATOR)

@app.route('/about')
def about():
    return render_template('about.html', creator=CREATOR)

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        # Extract form data
        handle = request.form.get('handle')
        skills = request.form.get('skills')
        message = request.form.get('message')
        passphrase = request.form.get('passphrase')
        
        # Validate passphrase
        if passphrase.lower() in ['debt', 'evil corp', 'the system']:
            # Save to database
            recruit = Recruit(
                handle=handle,
                skills=skills,
                message=message,
                passphrase=passphrase,
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string
            )
            db.session.add(recruit)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Application received. Standby for encrypted contact.'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Security check failed. Rethink your answer.'
            }), 400
            
    return render_template('join.html', creator=CREATOR)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Extract form data
        subject = request.form.get('subject')
        message = request.form.get('contact-message')
        pgp_key = request.form.get('pgp-key')
        
        # Save to database
        contact_msg = Contact(
            subject=subject,
            message=message,
            pgp_key=pgp_key,
            ip_address=request.remote_addr
        )
        db.session.add(contact_msg)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Message encrypted and sent through secure channels. Connection terminated.'
        })
        
    return render_template('contact.html', creator=CREATOR)

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'active',
        'message': 'FSociety is watching...',
        'creator': CREATOR
    })

@app.route('/admin')
def admin():
    # A simple admin page to view submissions - in a real app would require authentication
    recruits = Recruit.query.order_by(Recruit.timestamp.desc()).all()
    contacts = Contact.query.order_by(Contact.timestamp.desc()).all()
    return render_template('admin.html', recruits=recruits, contacts=contacts, creator=CREATOR)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', creator=CREATOR), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
