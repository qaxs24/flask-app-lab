from flask import Flask

app = Flask(__name__)

from app.portfolio import portfolio_bp
app.register_blueprint(portfolio_bp)

from app.products import products_bp
app.register_blueprint(products_bp)