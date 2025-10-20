from flask import Flask

app = Flask(__name__)

from app.portfolio import portfolio_bp
app.register_blueprint(portfolio_bp)