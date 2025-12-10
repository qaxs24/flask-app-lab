from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError, Optional
from flask_login import current_user
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Ім\'я користувача', 
                           validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', 
                             validators=[DataRequired()])
    confirm_password = PasswordField('Підтвердіть пароль', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватися')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Це ім\'я вже зайняте. Будь ласка, оберіть інше.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Цей email вже використовується. Будь ласка, оберіть інший.')

class ContactForm(FlaskForm):
    name = StringField('Ім\'я', 
                       validators=[DataRequired(), Length(min=4, max=10)])
    
    email = StringField('Email', 
                        validators=[DataRequired(), Email(message="Некоректний email")])
    
    phone = StringField('Телефон', 
                        validators=[DataRequired(), 
                                    Regexp(r'^\+380\d{9}$', 
                                           message="Телефон має бути у форматі +380XXXXXXXXX")])
    
    subject = SelectField('Тема', 
                          choices=[('tech', 'Технічне питання'), 
                                   ('sales', 'Питання по продажам'), 
                                   ('other', 'Інше')])
    
    message = TextAreaField('Повідомлення', 
                            validators=[DataRequired(), Length(max=500)])
    
    submit = SubmitField('Відправити')

class LoginForm(FlaskForm):
    username = StringField('Ім\'я користувача або Email', 
                           validators=[DataRequired()])
    
    password = PasswordField('Пароль', 
                             validators=[DataRequired(), Length(min=4, max=32)])
    
    remember = BooleanField('Запам\'ятати мене')
    
    submit = SubmitField('Увійти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Ім\'я користувача', 
                           validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    about_me = TextAreaField('Про мене', 
                             validators=[Length(max=500)])
    picture = FileField('Оновити фото профілю', 
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    
    current_password = PasswordField('Поточний пароль')
    new_password = PasswordField('Новий пароль', 
                                 validators=[Optional(), Length(min=4, max=32)])
    confirm_new_password = PasswordField('Підтвердіть новий пароль', 
                                         validators=[EqualTo('new_password', message='Паролі повинні співпадати')])
    
    submit = SubmitField('Оновити профіль')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Це ім\'я вже зайняте. Будь ласка, оберіть інше.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Цей email вже використовується. Будь ласка, оберіть інший.')