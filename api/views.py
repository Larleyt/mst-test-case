from flask import (
    Blueprint,
    jsonify,
    request
)
from flask.views import MethodView
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from . import db
from .models import Book, Transaction


api = Blueprint('api', __name__)


class BookAPI(MethodView):
    def get(self):
        price_gt = request.args.get('price_gt', 0)
        price_lt = request.args.get('price_lt')
        cat_id = request.args.get('cat_id')

        query = Book.query.filter(
            Book.price > price_gt
        )
        if cat_id is not None:
            query = query.filter(Book.category == cat_id)
        if price_lt is not None:
            query = query.filter(Book.price < price_lt)

        return jsonify([b.to_json() for b in query.all()])


class TransactionAPI(MethodView):
    def post(self):
        if not request.is_json:
            raise UnsupportedMediaType()

        json_data = request.get_json()
        books_ids = json_data["books_ids"]
        user_id = json_data["user_id"]

        if books_ids is None or user_id is None:
            raise BadRequest()

        t = Transaction(user_id=int(user_id))
        t.books.extend(Book.query.filter(Book.id.in_(books_ids)).all())
        t.set_total_price()

        db.session.add(t)
        db.session.commit()
        return jsonify(t.to_json())


api.add_url_rule(
    "/books",
    view_func=BookAPI.as_view("books")
)
api.add_url_rule("/transactions",
    view_func=TransactionAPI.as_view("transactions")
)
