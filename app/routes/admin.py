from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.db import get_db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db(current_app)
        admin_user = db.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
        db.close()
        
        if admin_user and check_password_hash(admin_user['password'], password):
            session['admin_logged_in'] = True
            session['username'] = username
            session['user_id'] = admin_user['id']
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
            
    return render_template('login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
        
    db = get_db(current_app)
    
    total_qrs = db.execute('SELECT COUNT(*) as count FROM qr_history').fetchone()['count']
    recent_qrs = db.execute('SELECT * FROM qr_history ORDER BY fecha DESC LIMIT 100').fetchall()
    
    admins = db.execute('SELECT id, username FROM admins').fetchall()
    db.close()
    
    return render_template('dashboard.html', total_qrs=total_qrs, recent_qrs=recent_qrs, admins=admins)

@admin_bp.route('/dashboard/add_user', methods=['POST'])
def add_user():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
        
    new_username = request.form.get('new_username')
    new_password = request.form.get('new_password')
    
    if new_username and new_password:
        db = get_db(current_app)
        try:
            db.execute('INSERT INTO admins (username, password) VALUES (?, ?)', 
                       (new_username, generate_password_hash(new_password)))
            db.commit()
            flash(f'Usuario {new_username} creado exitosamente.', 'success')
        except Exception as e:
            flash(f'Error al crear usuario: El nombre {new_username} probablemente ya exista.', 'error')
        finally:
            db.close()
    else:
        flash('Debes completar todos los campos para añadir un usuario.', 'error')
        
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/dashboard/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
        
    if session.get('user_id') == user_id:
        flash('No puedes eliminar tu propio usuario activo.', 'error')
        return redirect(url_for('admin.dashboard'))
        
    db = get_db(current_app)
    db.execute('DELETE FROM admins WHERE id = ?', (user_id,))
    db.commit()
    db.close()
    flash('Usuario eliminado exitosamente.', 'success')
    
    return redirect(url_for('admin.dashboard'))
