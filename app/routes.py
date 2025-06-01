from flask import Blueprint, render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User
from .models import User, Post
from .forms import LoginForm, UserForm, PostFrom, RegisterForm

main = Blueprint("main", __name__)

# Create Route
@main.route("/")
def index():
    posts = Post.query.order_by(Post.created_at)
    return render_template("index.html", posts=posts)


@main.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UserForm()
    id = current_user.id
    user = User.query.get_or_404(id)
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at).all()

    if request.method == "POST":
        user.name = request.form['name']
        user.email = request.form['email']
        try:
            db.session.commit()
            flash("Update profile successfully!")
        except:
            flash("Update profile failed!")
        finally:
            return redirect(url_for("main.profile"))
    else:
        return render_template("profile.html", form=form, posts=posts)


# List Users
@main.route("/users", methods=['GET'])
@login_required
def users():
    users = User.query.order_by(User.created_at)
    return render_template("users.html", users=users)


# Add New User
@main.route("/users/add", methods=['GET', 'POST'])
@login_required
def add_user():
    form = UserForm()

    if request.method == 'POST':
        # Validate Form
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()

            if user is None:
                password_hash = generate_password_hash(password)
                user = User(name=name, email=email, password=password_hash)

                db.session.add(user)
                db.session.commit()

                flash("Add new user successfully!")
                
                return redirect(url_for("main.users"))

    return render_template("add_user.html", form=form)


# Update User
@main.route("/users/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_user(id):
    form = UserForm()
    user = User.query.get_or_404(id)

    if request.method == "POST":
        user.name = request.form['name']
        user.email = request.form['email']
        try:
            db.session.commit()
            flash("Update user successfully!")
            return redirect(url_for("main.users"))
        except:
            flash("Update user failed!")
            return render_template("update_user.html", form=form, user=user)
    else:
        return render_template("update_user.html", form=form, user=user)


# Delete User
@main.route("/users/<int:id>/delete")
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)

    try:
        db.session.delete(user)
        db.session.commit()
        flash("Delete user successfully!")
    except:
        flash("Delete user failed!")
    finally:
        return redirect(url_for("main.users"))
    

# Login
@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        # Validate Form
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()

            if user is not None and user.verify_password(password):
                login_user(user)
                flash("Login successfully!")
                return redirect(url_for("main.profile"))
            else:
                 flash("Invalid email or password!")
                 return redirect(url_for("main.login"))
                 
    return render_template("login.html", form=form)


# Register
@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        # Validate Form
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()

            if user is None:
                password_hash = generate_password_hash(password)
                user = User(name=name, email=email, password=password_hash)

                db.session.add(user)
                db.session.commit()

                flash("Register a new account successfully!")
                
                return redirect(url_for("main.login"))

    return render_template("register.html", form=form)


# Logout
@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for("main.login"))

# Create Post
@main.route("/posts/add", methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostFrom()

    if request.method == 'POST':
        # Validate Form
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            
            user_id = current_user.id

            post = Post(title=title, content=content, user_id=user_id)

            db.session.add(post)
            db.session.commit()

            flash("Add new post successfully!")
            
            return redirect(url_for("main.profile"))

    return render_template("add_post.html", form=form)


# Get Post
@main.route("/posts/<int:id>")
def get_post(id):
    post = Post.query.get_or_404(id)
    return render_template("post.html", post=post)


# Edit Post
@main.route("/posts/<int:id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = PostFrom()
    post = Post.query.get_or_404(id)

    user_id = current_user.id

    if user_id == post.user_id:
        if request.method == "POST":
            post.title = request.form['title']
            post.content = request.form['content']
            try:
                db.session.commit()
                flash("Update post successfully!")
                return redirect(url_for("main.profile"))
            except:
                flash("Update post failed!")
                return render_template("edit_post.html", form=form, post=post)
        else:
            form.content.data = post.content
            return render_template("edit_post.html", form=form, post=post)
    else:
        flash("You aren't authorized to edit that post!")
        return redirect(url_for("main.index"))


# Delete Post
@main.route("/posts/<int:id>/delete")
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    user_id = current_user.id

    if user_id == post.user_id:
        try:
            db.session.delete(post)
            db.session.commit()
            flash("Delete post successfully!")
        except:
            flash("Delete post failed!")
        finally:
            return redirect(url_for("main.profile"))
    else:
        flash("You aren't authorized to delete that post!")
        return redirect(url_for("main.index"))
    

# Create Custom Error Page

# Invalid URL
@main.errorhandler(404)
def page_not_found(e):
    return render_template("page_not_found.html"), 404


# Internal Server Error
@main.errorhandler(500)
def internal_server_error(e):
    return render_template("internal_server_error.html"), 500