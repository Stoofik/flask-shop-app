from flask import Flask, render_template, session, request, redirect, url_for, flash, request, current_app
from app import app, db
from products.models import Addproduct
from products.routes import brands, categories
import simplejson as json


def merge_dicts(dict1, dict2):
    if isinstance (dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route("/carts")
def get_cart():
    if "Shoppingcart" not in session or len(session["Shoppingcart"]) <= 0:
        flash("V košíku zatím nemáte žádný produkt", "danger")
        return redirect(url_for("home"))
    subtotal = 0
    grandtotal = 0
    for key, product in session["Shoppingcart"].items():
        discount = (product["discount"]/100 * float(product["price"]))
        subtotal += float(product["price"]) * int(product["quantity"])
        subtotal -= discount
        tax = ("%.2f" % (.15 * float(subtotal)))
        grandtotal = float("%.2f" % (1.15 * subtotal))
    return render_template("products/carts.html", grandtotal= grandtotal, tax=tax, brands=brands(), categories=categories(), title="Nákupní košík")


@app.route("/addcart", methods=["POST"])
def add_cart():
    try:
        product_id = request.form.get("product_id")
        quantity = int(request.form.get("quantity"))
        colors = request.form.get("colors")
        product = Addproduct.query.filter_by(id=product_id).first()
        if product_id and quantity and colors and request.method=="POST":
            DictItems = {
                product_id:{
                    "name" : product.name,
                    "price" : float(product.price),
                    "discount" : product.discount,
                    "color" : colors,
                    "quantity" : quantity,
                    "image" : product.image_1,
                    "colors" : product.colors
                    }
            }
            if "Shoppingcart" in session:
                print(session["Shoppingcart"])
                if product_id in session["Shoppingcart"]:
                    for key, item in session["Shoppingcart"].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            flash(f"Produkt {product.name} přidán do košíku","success")
                            item["quantity"] += 1
                else:
                    session["Shoppingcart"] = merge_dicts(session["Shoppingcart"], DictItems)
                    flash(f"Produkt {product.name} přidán do košíku","success")
                    return redirect(request.referrer)
            else:
                session["Shoppingcart"] = DictItems
                flash(f"Produkt {product.name} přidán do košíku","success")
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route("/updatecart<int:code>", methods=["POST"])
def update_cart(code):
    if "Shoppingcart" not in session or len(session["Shoppingcart"]) <= 0:
        return redirect(url_for("home"))
    if request.method=="POST":
        quantity = request.form.get("quantity")
        color = request.form.get("color")
        try:
            session.modified = True
            for key, item in session["Shoppingcart"].items():
                if int(key) == code:
                    item["quantity"] = quantity
                    item["color"] = color
                    flash("Změny byly provedeny", "success")
                    return redirect(url_for("get_cart"))
        except Exception as e:
            print(e)
            return redirect(url_for("get_cart"))
    


@app.route("/deleteitem/<int:id>")
def delete_item(id):
    if "Shoppingcart" not in session or len(session["Shoppingcart"]) <=0:
        return redirect(url_for("home"))
    try:
        session.modified = True
        for key, item in session["Shoppingcart"].items():
            if int(key) == id:
                session["Shoppingcart"].pop(key, None)
                return redirect(url_for("get_cart"))
    except Exception as e:
            print(e)
            return redirect(url_for("get_cart"))


@app.route("/clearcart")
def clear_cart():
    try:
        session.pop("Shoppingcart", None)
        return redirect(url_for("home"))
    except Exception as e:
        print(e)
        return redirect(url_for("home"))


