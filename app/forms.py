from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp

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
                             validators=[DataRequired(), Length(min=4, max=10)])
    
    remember = BooleanField('Запам\'ятати мене')
    
    submit = SubmitField('Увійти')