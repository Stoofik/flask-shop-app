from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
#from flask_msearch import Search
from flask_migrate import Migrate
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = "000abcdefghijk123456000"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir, "static/images")

photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)
patch_request_class(app)
# search = Search()
# search.init_app(app)




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "customer_login"
login_manager.needs_refresh_message_category = "danger"
login_manager.login_message = u"Prosím přihlašte se"
login_manager.login_message_category = "danger"


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


from admin import routes
from products import routes
from carts import carts
from customers import routes

