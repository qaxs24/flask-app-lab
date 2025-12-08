from flask import render_template, redirect, url_for, flash, current_app
from app.portfolio import portfolio_bp
from app.forms import ContactForm
from app import db
from app.models import Feedback

@portfolio_bp.route('/')
@portfolio_bp.route('/resume')
def resume():
    return render_template('portfolio/resume.html', title="Резюме")

@portfolio_bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        
        feedback = Feedback(
            name=name,
            email=email,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(feedback)
        db.session.commit()
        
        current_app.logger.info(f"New contact form submission from {name} ({email}): {form.message.data}")
        
        flash(f'Дякуємо, {name}! Ваше повідомлення було успішно надіслано.', 'success')
        return redirect(url_for('portfolio.contacts'))
    
    return render_template('portfolio/contacts.html', title="Контакти", form=form)