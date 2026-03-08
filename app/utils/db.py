import sqlite3
import os
from werkzeug.security import generate_password_hash

def get_db(app):
    db_path = os.path.join(app.root_path, '..', 'qr_generator.db')
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    return db

def init_db(app):
    with app.app_context():
        db = get_db(app)
        db.execute('''
            CREATE TABLE IF NOT EXISTS qr_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT NOT NULL,
                tipo INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        # Create default admin if not exists
        admin = db.execute('SELECT * FROM admins WHERE username = ?', ('admin',)).fetchone()
        if not admin:
            db.execute('INSERT INTO admins (username, password) VALUES (?, ?)',
                       ('admin', generate_password_hash('admin123')))
            
        db.commit()
        db.close()
