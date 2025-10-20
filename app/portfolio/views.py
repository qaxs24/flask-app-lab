from flask import render_template
from app.portfolio import portfolio_bp

@portfolio_bp.route('/')
@portfolio_bp.route('/resume')
def resume():
    return render_template('portfolio/resume.html', title="Резюме")

@portfolio_bp.route('/contacts')
def contacts():
    return render_template('portfolio/contacts.html', title="Контакти")