from flask import Blueprint

portfolio_bp = Blueprint(
    'portfolio', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/portfolio/static'
)

from app.portfolio import views