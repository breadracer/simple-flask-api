from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Shawn'

api = Api(app)

jwt = JWT(app, authenticate, identity)



storeList = [
    {
        'name': 'stationery',
        'items': [
            {
                'name': 'pencil',
                'price': 10
            },
            {
                'name': 'eraser',
                'price': 15
            }
        ]
    },
    {
        'name': 'food',
        'items': [
            {
                'name': 'pork',
                'price': 30
            },
            {
                'name': 'sugar',
                'price': 5
            }
        ]
    }
]

class StoreList(Resource):
    
    @jwt_required()
    def get(self):
        return {'storeList': storeList}

    @jwt_required()
    def post(self):
         data = request.get_json()
         for store in storeList:
             if store['name'] == data['name']:
                 return {'message': 'Store named {} already exists'.format(store['name'])}, 400
         newStore = {
            'name': data['name'],
            'items': list(map(lambda item:
                {
                    'name': item['name'],
                    'price': item['price']
                },
                data['items']))
         }
         storeList.append(newStore)
         return newStore, 201
        

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('price', type=float, required=True)

    @jwt_required()
    def get(self, name):
        for store in storeList:
            if store['name'] == name:
                return store, 200
        return {'message': 'Store named {} is not found'.format(name)}, 404

    @jwt_required()
    def post(self, name):
        data = Store.parser.parse_args()
        newItem = {
            'name': data['name'],
            'price': data['price']
        }
        for store in storeList:
            if store['name'] == name:
                for item in store['items']:
                    if item['name'] == newItem['name']:
                        return {'message': 'Item already exists'}, 400
                    store['items'].append(newItem)
                    return newItem, 201
        return {'message': 'Store named {} not found'.format(name)}, 404

class Item(Resource):
    @jwt_required()
    def get(self, name, itemName):
        for store in storeList:
            if store['name'] == name:
                for item in store['items']:
                    if item['name'] == itemName:
                        return item, 200
                return {'message': 'Item named {} not found'.format(itemName)}, 404
        return {'message': 'Store named {} not found'.format(name)}, 404

        
api.add_resource(StoreList, '/api')
api.add_resource(Store, '/api/store/<string:name>')
api.add_resource(Item, '/api/store/<string:name>/item/<string:itemName>')

app.run(port=5001, debug=True)
