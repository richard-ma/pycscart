from flask import Flask, request
from flask_restful import Resource, Api, abort
import json

app = Flask(__name__)
api = Api(app)
db = dict()

def load_orders(filename):
    db['orders'] = list()
    with open(filename, 'r') as f:
        for line in f.readlines():
            db['orders'].append(json.loads(line))

class Orders(Resource):
    def get(self):
        res = {'orders': db['orders']}
        return res

    def post(self):
        return {'type': 'post'}

class Order(Resource):
    def get(self, order_id):
        for order in db['orders']:
            if order['order_id'] == order_id:
                return order
        abort(404)

    def put(self):
        return {'type': 'put'}

    def delete(self, order_id):
        for idx, order in enumerate(db['orders']):
            if order['order_id'] == order_id:
                del db['orders'][idx]
                return '', 204
        abort(404)

api.add_resource(Orders, '/api/orders')
api.add_resource(Order, '/api/orders/<order_id>')

if __name__ == "__main__":
    load_orders("./test/fake-server/order.dat")
    app.run(debug=True)
