from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import hashlib

load_dotenv()

app = Flask(__name__)
CORS(app)

# Security
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
DB_FILE = 'portfolio.db'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY,
        hero_name TEXT,
        hero_sub TEXT,
        hero_bio TEXT,
        stats TEXT,
        experience TEXT,
        skills TEXT,
        education TEXT,
        languages TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY,
        token TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def generate_token():
    """Generate a simple session token"""
    import secrets
    return secrets.token_urlsafe(32)

# Routes
@app.route('/api/verify-password', methods=['POST'])
def verify_password():
    """Verify admin password and return token"""
    data = request.get_json()
    password = data.get('password', '')
    
    if hashlib.sha256(password.encode()).hexdigest() == hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest():
        token = generate_token()
        conn = get_db_connection()
        c = conn.cursor()
        
        # Store token (valid for 24 hours)
        from datetime import timedelta
        expires = datetime.now() + timedelta(hours=24)
        c.execute('INSERT INTO sessions (token, expires_at) VALUES (?, ?)', (token, expires))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'token': token}), 200
    else:
        return jsonify({'success': False, 'message': 'Incorrect password'}), 401

@app.route('/api/verify-token', methods=['POST'])
def verify_token():
    """Verify if session token is valid"""
    data = request.get_json()
    token = data.get('token', '')
    
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM sessions WHERE token = ? AND expires_at > datetime("now")', (token,))
    session = c.fetchone()
    conn.close()
    
    if session:
        return jsonify({'valid': True}), 200
    else:
        return jsonify({'valid': False}), 401

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Get all portfolio data"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM portfolio ORDER BY updated_at DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    
    if row:
        return jsonify({
            'hero_name': row['hero_name'],
            'hero_sub': row['hero_sub'],
            'hero_bio': row['hero_bio'],
            'stats': json.loads(row['stats']) if row['stats'] else [],
            'experience': json.loads(row['experience']) if row['experience'] else [],
            'skills': json.loads(row['skills']) if row['skills'] else [],
            'education': json.loads(row['education']) if row['education'] else {},
            'languages': json.loads(row['languages']) if row['languages'] else []
        }), 200
    else:
        return jsonify({}), 200

@app.route('/api/portfolio', methods=['POST'])
def save_portfolio():
    """Save portfolio data (requires auth token)"""
    # Verify token
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM sessions WHERE token = ? AND expires_at > datetime("now")', (token,))
    session = c.fetchone()
    
    if not session:
        conn.close()
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    c.execute('''INSERT INTO portfolio 
        (hero_name, hero_sub, hero_bio, stats, experience, skills, education, languages) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (
            data.get('hero_name', ''),
            data.get('hero_sub', ''),
            data.get('hero_bio', ''),
            json.dumps(data.get('stats', [])),
            json.dumps(data.get('experience', [])),
            json.dumps(data.get('skills', [])),
            json.dumps(data.get('education', {})),
            json.dumps(data.get('languages', []))
        )
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Portfolio saved'}), 200

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
