from flask import render_template
from app.products import products_bp

products_list = [
    {"id": 1, "name": "Laptop", "description": "Потужний ноутбук для роботи"},
    {"id": 2, "name": "Smartphone", "description": "Сучасний смартфон з чудовою камерою"},
]

@products_bp.route('/products')
def products():
    return render_template('products/products.html', title="Товари", products=products_list)