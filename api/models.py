from sqlalchemy.orm import synonym

from . import db


books = db.Table('books',
    db.Column(
        'book_id',
        db.Integer,
        db.ForeignKey('book.id'),
        primary_key=True
    ),
    db.Column(
        'transaction_id',
        db.Integer,
        db.ForeignKey('transaction.id'),
        primary_key=True
    )
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True,)
    email = db.Column(db.String(120), nullable=False, unique=True,)
    phone = db.Column(db.String(20), nullable=True)
    transactions = db.relationship("Transaction", backref="user")

    def __repr__(self):
        return '<User %r>' % self.username


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    books = db.relationship("Book", backref="category")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def __repr__(self):
        return '<Category %r>' % self.name


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category.to_json(),
        }

    def __repr__(self):
        return '<Book %r>' % self.name


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    books = db.relationship('Book', secondary=books, lazy='subquery',
        backref=db.backref('transactions', lazy=True))
    _total_price = db.Column(db.Float, nullable=False)

    def get_total_price(self):
        return self._total_price

    def set_total_price(self):
        self._total_price = sum((b.price for b in self.books))

    def to_json(self):
        return {
            "id": self.id,
            "books": [b.to_json() for b in self.books],
            "user_id": self.user_id,
            "total_price": self.get_total_price()
        }

    def __repr__(self):
        return '<Transaction %r>' % self.id
