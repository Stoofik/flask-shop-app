from flask import Flask, render_template, session, request, redirect, url_for, flash, request, current_app
from app import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets, os


def brands():
    brands = Brand.query.all()
    return brands


def categories():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories


@app.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=9)
    return render_template("products/index.html", products = products, brands = brands(), categories=categories(), title="Julči domácí výrobky")


@app.route("/product/<int:id>")
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template("products/single_page.html", product=product, categories=categories())

@app.route("/brand/<int:id>")
def get_brand(id):
    get_brand = Brand.query.filter_by(id=id).first_or404_()
    return render_template("products/index.html", brand=get_brand())


@app.route("/categories/<int:id>")
def get_category(id):
    get_cat = Category.query.filter_by(id=id).first_or_404()
    page = request.args.get("page", 1, type=int)
    category = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=9)
    return render_template("products/index.html", category=category, categories=categories(), get_cat=get_cat)



@app.route("/addbrand", methods=["GET", "POST"])
def addbrand():
    if "email" not in session:
        flash(f"Nejprve se přihlašte", "danger")
        return redirect(url_for("login"))
    if request.method == "POST":
        getbrand = request.form.get("brand")
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f"Značka {getbrand} byla přidána do databáze", "success")
        db.session.commit()
        return redirect(url_for("addbrand"))
    return render_template("products/addbrand.html", brands="brands", title="Přidat značku")


@app.route("/updatebrand/<int:id>", methods=["GET", "POST"])
def updatebrand(id):
    if "email" not in session:
        flash(f"Nejprve se přihlašte", "danger")
        return redirect(url_for("login"))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get("brand")
    if request.method == "POST":
        updatebrand.name = brand
        flash(f"Značka byla změněna", "success")
        db.session.commit()
        return redirect(url_for("brands"))
    return render_template("products/updatebrand.html", title="Upravit značku", updatebrand=updatebrand)


@app.route("/deletebrand/<int:id>", methods=["POST"])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f"Značka {brand.name} byla odstraněna z databáze", "success")
        return redirect(url_for("admin"))
    flash(f"Značka {brand.name} nemůže být odstraněna", "warning")
    return redirect(url_for("admin"))

@app.route("/addcat", methods=["GET", "POST"])
def addcat():
    if "email" not in session:
        flash(f"Nejprve se přihlašte", "danger")
        return redirect(url_for("login"))
    if request.method == "POST":
        getbrand = request.form.get("category")
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f"Kategorie {getbrand} byla přidána do databáze", "success")
        db.session.commit()
        return redirect(url_for("addcat"))
    return render_template("products/addbrand.html", title="Přidat kategorii")


@app.route("/updatecat/<int:id>", methods=["GET", "POST"])
def updatecat(id):
    if "email" not in session:
        flash(f"Nejprve se přihlašte", "danger")
        return redirect(url_for("login"))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get("category")
    if request.method == "POST":
        updatecat.name = category
        flash(f"Kategorie byla změněna", "success")
        db.session.commit()
        return redirect(url_for("category"))
    return render_template("products/updatebrand.html", title="Upravit značku", updatecat=updatecat)


@app.route("/deletecategory/<int:id>", methods=["POST"])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        db.session.commit()
        flash(f"Kategorie {category.name} byla odstraněna z databáze", "success")
        return redirect(url_for("admin"))
    flash(f"Kategorie {category.name} nemůže být odstraněna", "warning")
    return redirect(url_for("admin"))


@app.route("/addproduct", methods=["GET", "POST"])
def addproduct():
    if "email" not in session:
        flash(f"Nejprve se přihlašte", "danger")
        return redirect(url_for("login"))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.description.data
        brand = request.form.get("brand")
        category = request.form.get("category")
        image_1 = photos.save(request.files.get("image_1"), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get("image_2"), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get("image_3"), name=secrets.token_hex(10) + ".")
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, colors=colors,desc=desc, brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f"Produkt {name} byl přidán to databáze", "success")
        db.session.commit()
        return redirect(url_for("admin"))

    return render_template("products/addproduct.html", form=form, title="Přidat produkt", brands=brands, categories=categories)


@app.route("/updateproduct<int:id>", methods=["GET", "POST"])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get("brand")
    category = request.form.get("category")
    form = Addproducts(request.form)
    if request.method =="POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.desc = form.description.data
        if request.files.get("image_1"):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get("image_1"), name=secrets.token_hex(10) + ".")
            except:
                photos.save(request.files.get("image_1"), name=secrets.token_hex(10) + ".")

        if request.files.get("image_2"):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get("image_2"), name=secrets.token_hex(10) + ".")
            except:
                photos.save(request.files.get("image_2"), name=secrets.token_hex(10) + ".")
        if request.files.get("image_3"):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get("image_3"), name=secrets.token_hex(10) + ".")
            except:
                photos.save(request.files.get("image_3"), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f"Produkt byl upraven", "success")
        return redirect(url_for("admin"))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.desc


    return render_template("products/updateproduct.html", form=form, brands=brands, categories=categories, product=product)


@app.route("/deleteproduct/<int:id>", methods=["POST"])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)

        db.session.delete(product)
        db.session.commit()
        flash(f"Produkt {product.name} byl odstraněn z databáze", "success")
        return redirect(url_for("admin"))
    flash(f"Produkt {product.name} nemůže být odstraněn")

    return redirect(url_for("admin"))


