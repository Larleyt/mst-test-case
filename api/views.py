from flask import (
    Blueprint,
    jsonify,
    redirect,
    request
)
from flask.views import MethodView

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
        pass


api.add_url_rule(
    "/books",
    view_func=BookAPI.as_view("books"),
    methods=['GET']
)
api.add_url_rule("/transactions",
    view_func=TransactionAPI.as_view("transactions"),
    methods=['POST']
)
