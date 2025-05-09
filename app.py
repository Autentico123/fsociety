from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

# Creator attribution 
CREATOR = "Asero"

@app.route('/')
def index():
    return render_template('index.html', creator=CREATOR)

@app.route('/about')
def about():
    return render_template('about.html', creator=CREATOR)

@app.route('/join')
def join():
    return render_template('join.html', creator=CREATOR)

@app.route('/contact')
def contact():
    return render_template('contact.html', creator=CREATOR)

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'active',
        'message': 'FSociety is watching...',
        'creator': CREATOR
    })

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', creator=CREATOR), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
