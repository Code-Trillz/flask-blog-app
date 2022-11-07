from flask import *
from flask_login import login_required, current_user
from .models import Post, User, Comment
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", user = current_user, posts = posts)

@views.route("/create-post", methods = ["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")

        if not text:
            flash("Insert text to post an article!", category="error")
        else:
            post = Post(text = text, author = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("article created successfully", category="success")
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user = current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id = id).first()

    if not post:
        flash("post does not exist", category="error")
    elif current_user.id == post.id:
        flash("permission denied", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("deleted successfully", category="success")

    return redirect(url_for("views.home"))

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("oops!!, username does not exist", category="error")
        return redirect(url_for("views.home"))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)

@views.route("create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get("text")

    if not text:
        flash("cannot post empty comment", category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash("comment added successfully", category="success")
        else:
            flash("post does not exist", category="error")

    return redirect(url_for("views.home"))

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash("comment does not exist.", category="error")
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash("permission denied!", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("comment deleted", category="success")

    return redirect(url_for("views.home"))


