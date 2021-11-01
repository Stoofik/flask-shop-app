from flask import Flask, render_template, session, request, redirect, url_for, flash, request, current_app
from app import db, app, photos, bcrypt, login_manager
from flask_login import login_required, login_user, logout_user, current_user
from .forms import CustomerRegisterForm, CustomerLoginForm, UpdateAccountForm
from .models import Register, CustomerOrder
from products.routes import brands, categories
import secrets, os
import stripe


publishable_key = "pk_test_51IXlX7Ffc8ZAZaBUzoXHr4ZGwoIBbxjw9LLrF7J2jUaSQq5lgzqDWPMFgnKTWLLFQYSDMVrxxsF3QJfc3kP6RlOA00dFdzpiws"

stripe.api_key = "sk_test_51IXlX7Ffc8ZAZaBUTfez3AYk0K8dn3r30aotDYiS7aitNaytKikBkxiAWBgcQ78vlWDdWOeUN0u5qZFZ8HJYSmmz00ECk0groF"

@app.route("/payment", methods=["POST"])
@login_required
def payment():
    invoice = request.form.get("invoice")
    amount = request.form.get("amount")
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Julči obchod',
        amount=amount,
        currency='czk',
    )
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id).order_by(CustomerOrder.id.desc()).first()
    orders.status = "Zaplaceno"
    db.session.commit()
    return redirect(url_for("thanks"))


@app.route("/thanks")
def thanks():
    return render_template("customer/thanks.html")

@app.route("/customer/register", methods=["GET", "POST"])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(username=form.username.data, surname=form.surname.data, last_name=form.last_name.data, email=form.email.data, password=hash_password, 
        contact=form.contact.data, country=form.country.data, city=form.city.data, adress=form.adress.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f"Profil úspěšně vytvořen pro {form.username.data}. Děkujeme", "success")
        db.session.commit()
        return redirect(url_for("customer_login"))
    return render_template("customer/register.html", form=form, categories=categories())


@app.route("/customer/login", methods=["GET", "POST"])
def customer_login():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Přihlášení úspěšné", "success")
            next = request.args.get("next")
            return redirect(next or url_for("home"))
        flash("Neplatný email a heslo", "danger")
        return redirect(url_for("customer_login"))
    return render_template("customer/login.html", form=form, categories=categories())


@app.route("/customer/logout")
def customer_logout():
    logout_user()
    return redirect(url_for("home"))


#remove unwanted details from shopping cart
def update_shopping_cart():
    for _key, product in session["Shoppingcart"].items():
        session.modified = True
        del product["image"]
        del product["colors"]
    return update_shopping_cart


@app.route("/getorder")
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        update_shopping_cart()
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session["Shoppingcart"])
            db.session.add(order)
            db.session.commit()
            session.pop("Shoppingcart")
            flash("Objednávka byla úspěšně odeslána", "success")
            return redirect(url_for("orders",invoice=invoice))
        except Exception as e:
            print(e)
            flash("Něco se nepovedlo při vytváření objednávky", "danger")
            return redirect(url_for("get_cart"))

@app.route("/orders/<invoice>")
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product["discount"]/100) * float(product["price"])
            subTotal += float(product["price"]) * int(product["quantity"])
            subTotal -= discount
            tax = float("%.2f" % (.06 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * float(subTotal)))
    
    else:
        return redirect(url_for("customer_login"))

    return render_template("customer/order.html", invoice=invoice, tax=tax, subTotal=subTotal, grandTotal=grandTotal,
            customer=customer, orders=orders)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def customer_profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.surname = form.surname.data
        current_user.last_name = form.last_name.data
        current_user.contact = form.contact.data
        current_user.country = form.country.data
        current_user.city = form.city.data
        current_user.adress = form.adress.data
        current_user.zipcode = form.zipcode.data
        db.session.commit()
        flash("Změny provedeny", "success")
        return redirect(url_for("customer_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.surname.data = current_user.surname
        form.last_name.data = current_user.last_name
        form.contact.data = current_user.contact
        form.country.data = current_user.country
        form.city.data = current_user.city
        form.adress.data = current_user.adress
        form.zipcode.data = current_user.zipcode
    return render_template("customer/profile.html", title="Správa profilu", form=form, categories=categories())

