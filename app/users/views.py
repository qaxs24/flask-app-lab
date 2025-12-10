from flask import render_template, request, redirect, url_for, session, flash, make_response, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app.users import users_bp
from app.forms import LoginForm, RegistrationForm, UpdateAccountForm
from app.models import User
from app import db
from datetime import datetime
import secrets
import os
from PIL import Image


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
    
    output_size = (128, 128)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn


@users_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Ваш акаунт створено! Тепер ви можете увійти', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Реєстрація', form=form)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash_message = f'Ви успішно увійшли як {user.username}.'
            if form.remember.data:
                flash_message += ' Опція "Запам\'ятати мене" була обрана.'
            
            flash(flash_message, 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash('Неправильне ім\'я користувача або пароль.', 'danger')
            return redirect(url_for('users.login'))
            
    return render_template('users/login.html', title="Вхід", form=form)

@users_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    
    if request.method == 'POST':
        if request.form.get('cookie_action'):
            action = request.form.get('action')
            resp = make_response(redirect(url_for('users.account')))

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
        
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image = picture_file
            
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.about_me = form.about_me.data
            
            if form.new_password.data:
                if form.current_password.data:
                    if current_user.check_password(form.current_password.data):
                        current_user.set_password(form.new_password.data)
                        flash('Пароль успішно змінено!', 'success')
                    else:
                        flash('Поточний пароль невірний.', 'danger')
                        return render_template('users/account.html', title="Профіль", form=form)
                else:
                    flash('Для зміни пароля введіть поточний пароль.', 'warning')
                    return render_template('users/account.html', title="Профіль", form=form)
            
            db.session.commit()
            flash('Ваш профіль оновлено!', 'success')
            return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    
    return render_template('users/account.html', title="Профіль", form=form)

@users_bp.route('/users')
@login_required
def users_list():
    users = User.query.all()
    count = User.query.count()
    return render_template('users/users_list.html', users=users, count=count, title="Користувачі")

@users_bp.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/change-theme/<theme>')
def change_theme(theme):
    resp = make_response(redirect(request.referrer or url_for('users.account')))
    if theme in ['light', 'dark']:
        resp.set_cookie('theme', theme, max_age=60*60*24*30)
        flash(f'Тему змінено на "{theme}".', 'info')
    return resp