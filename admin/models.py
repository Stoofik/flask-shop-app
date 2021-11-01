from app import db


class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)

    def __repr__(self):
        return f"AdminUser('{self.id}', '{self.username}', '{self.email}')"

db.create_all()