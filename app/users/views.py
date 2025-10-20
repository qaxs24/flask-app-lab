from flask import render_template, request, redirect, url_for, session, flash
from app.users import users_bp

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'password':
            session['username'] = username
            flash('Ви успішно увійшли!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Неправильне ім\'я користувача або пароль.', 'danger')
    
    return render_template('users/login.html', title="Вхід")

@users_bp.route('/profile')
def profile():
    if 'username' not in session:
        flash('Будь ласка, увійдіть, щоб побачити цю сторінку.', 'warning')
        return redirect(url_for('users.login'))
    
    return render_template('users/profile.html', title="Профіль")

@users_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))