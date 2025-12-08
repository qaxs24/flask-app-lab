from flask import render_template, request, redirect, url_for, session, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from app.users import users_bp
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app import db

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш акаунт створено! Тепер ви можете увійти', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Реєстрація', form=form)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash_message = f'Ви успішно увійшли як {user.username}.'
            if form.remember.data:
                flash_message += ' Опція "Запам\'ятати мене" була обрана.'
            
            flash(flash_message, 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.profile'))
        else:
            flash('Неправильне ім\'я користувача або пароль.', 'danger')
            return redirect(url_for('users.login'))
            
    return render_template('users/login.html', title="Вхід", form=form)

@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        action = request.form.get('action')
        resp = make_response(render_template('users/profile.html', title="Профіль"))

        if action == 'add_cookie':
            key = request.form.get('cookie_key')
            value = request.form.get('cookie_value')
            expiry = request.form.get('cookie_expiry')
            if key and value:
                max_age = int(expiry) if expiry else None
                resp.set_cookie(key, value, max_age=max_age)
                flash(f'Кукі "{key}" було успішно додано.', 'success')
            else:
                flash('Ключ та значення для кукі є обов\'язковими.', 'warning')

        elif action == 'delete_cookie':
            key_to_delete = request.form.get('cookie_key_to_delete')
            if key_to_delete in request.cookies:
                resp.delete_cookie(key_to_delete)
                flash(f'Кукі "{key_to_delete}" було видалено.', 'info')
            else:
                flash(f'Кукі з ключем "{key_to_delete}" не знайдено.', 'warning')
        
        elif action == 'delete_all_cookies':
            for key in request.cookies:
                if key != 'session': 
                    resp.delete_cookie(key)
            flash('Усі ваші кукі було видалено.', 'info')
        
        return resp

    return render_template('users/profile.html', title="Профіль")

@users_bp.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/change-theme/<theme>')
def change_theme(theme):
    resp = make_response(redirect(request.referrer or url_for('users.profile')))
    if theme in ['light', 'dark']:
        resp.set_cookie('theme', theme, max_age=60*60*24*30)
        flash(f'Тему змінено на "{theme}".', 'info')
    return resp