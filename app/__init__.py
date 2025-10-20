from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_very_secret_key_that_should_be_changed'

from app.portfolio import portfolio_bp
app.register_blueprint(portfolio_bp)

from app.products import products_bp
app.register_blueprint(products_bp)

from app.users import users_bp
app.register_blueprint(users_bp)