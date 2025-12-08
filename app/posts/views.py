from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.posts import post_bp
from app.posts.forms import PostForm
from app.posts.models import Post, CategoryEnum
from datetime import datetime

@post_bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=CategoryEnum[form.category.data],
            is_active=form.enabled.data,
            posted=form.publish_date.data,
            author=current_user.username if current_user.is_authenticated else 'Anonymous'
        )
        db.session.add(post)
        db.session.commit()
        flash('Пост успішно створено!', 'success')
        return redirect(url_for('post.all_posts'))
    
    # Set default date for new post
    if request.method == 'GET':
        form.publish_date.data = datetime.now()
        
    return render_template('posts/add_post.html', title='Новий пост', form=form, legend='Новий пост')

@post_bp.route('/post')
def all_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template('posts/all_posts.html', posts=posts)

@post_bp.route('/post/<int:id>')
def detail_post(id):
    post = Post.query.get_or_404(id)
    return render_template('posts/detail_post.html', title=post.title, post=post)

@post_bp.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = CategoryEnum[form.category.data]
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data
        db.session.commit()
        flash('Пост оновлено!', 'success')
        return redirect(url_for('post.detail_post', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category.name
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted
        
    return render_template('posts/add_post.html', title='Редагувати пост', form=form, legend='Редагувати пост')

@post_bp.route('/post/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Пост видалено!', 'success')
        return redirect(url_for('post.all_posts'))
    return render_template('posts/delete_confirm.html', post=post)
