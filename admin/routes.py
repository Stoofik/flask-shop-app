from flask import Flask, render_template, session, request, redirect, url_for, flash
from app import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import AdminUser
from products.models import Addproduct, Brand, Category
import os


@app.route("/admin")
def admin():
    if "email" not in session:
        flash(f"Nejprve se přihlašte", "danger")
        return redirect(url_for("login"))
    products = Addproduct.query.all()
    return render_template("admin/index.html", title="Admin Page", products=products)


@app.route("/brands")
def brands():
    if "email" not in session:
        flash(f"Nejprve se přihlašte", "danger")
        return redirect(url_for("login"))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template("admin/brand.html", title="Stránka značek", brands=brands)


@app.route("/category")
def category():
    if "email" not in session:
        flash(f"Nejprve se přihlašte", "danger")
        return redirect(url_for("login"))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template("admin/brand.html", title="Stránka značek", categories=categories)


@app.route("/admin/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = AdminUser(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Byl vytvořen účet pro uživatele {form.username.data}.", "success")
        return redirect(url_for("admin"))
    return render_template("admin/register.html", title="Založení nového Admin uživatele", form=form)


@app.route("/admin/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(email = form.email.data).first()
        if form.email.data == "Admin@admin.com" and bcrypt.check_password_hash(user.password, form.password.data):
            session["email"] = form.email.data
            flash(f"Vítejte {form.usernam.data}", "success")
            return redirect(request.args.get("next") or url_for("admin"))
        else:
            flash("Email a heslo nesouhlasí, prosím zkuste to znovu", "danger")
            return redirect(url_for("login"))
    return render_template("admin/login.html", form=form, title="Přihlášení uživatele")


@app.route("/admin/logout")
def admin_logout():
    try:
        session.pop("email", None)
        return redirect(url_for("home"))
    except Exception as e:
        print(e)
        return redirect(url_for("home"))

