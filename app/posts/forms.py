from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired
from app.posts.models import CategoryEnum

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Зміст', validators=[DataRequired()])
    category = SelectField('Категорія', choices=[(choice.name, choice.value) for choice in CategoryEnum], validators=[DataRequired()])
    enabled = BooleanField('Активний')
    publish_date = DateTimeLocalField('Дата публікації', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Зберегти')
