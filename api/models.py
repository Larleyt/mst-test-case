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

    def __repr__(self):
        return '<User %r>' % self.username


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return '<Category %r>' % self.name


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
        }

    def __repr__(self):
        return '<Book %r>' % self.name


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    books = db.relationship('Book', secondary=books, lazy='subquery',
        backref=db.backref('transactions', lazy=True))
    _total_price = db.Column(db.Float, nullable=False)

    @property
    def total_price(self):
        return self._total_price

    @total_price.setter
    def total_price(self):
        self._total_price = sum((book.price for book in self.books))

    total_price = synonym('_total_price', descriptor=total_price)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "total_price": self.total_price
        }


    def __repr__(self):
        return '<Transaction %r>' % self.id
