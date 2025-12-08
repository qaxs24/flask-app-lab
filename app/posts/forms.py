from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, DateTimeLocalField, SelectMultipleField
from wtforms.validators import DataRequired
from app.posts.models import CategoryEnum, Tag
from app.models import User

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Зміст', validators=[DataRequired()])
    category = SelectField('Категорія', choices=[(choice.name, choice.value) for choice in CategoryEnum], validators=[DataRequired()])
    author_id = SelectField('Автор', coerce=int)
    tags = SelectMultipleField('Теги', coerce=int)
    enabled = BooleanField('Активний')
    publish_date = DateTimeLocalField('Дата публікації', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Зберегти')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_id.choices = [(u.id, u.username) for u in User.query.order_by(User.username).all()]
        self.tags.choices = [(t.id, t.name) for t in Tag.query.order_by(Tag.name).all()]
