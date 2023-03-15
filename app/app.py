import os
import json
from flask import Flask,  request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import DateTime, Float, Integer
from flask_migrate import Migrate
from serializers import AlchemyEncoder
import datetime
# create an instance of flask
app = Flask(__name__)
# creating an API object
api = Api(app)
# create database
# f'mysql://{user}:{password}@{host}/{database}'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', '43509910'),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://flask:slimdingo85@localhost:3306/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# sqlalchemy mapper

db = SQLAlchemy(app)
#Para generar tablas
migrate = Migrate(app, db)

# models
class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    image = db.Column("image", db.String(200))
    price = db.Column("price", db.Float)
    stard_date = db.Column("start_date", DateTime)
    ending_date = db.Column("ending_date", DateTime)
    quantity = db.Column("quantity", db.Integer)
    #datetime = db.Column("datetime", DateTime)
    def __repr__(self):
        return f"({self.id}) name: {self.name}, price: {self.price}, stard_date: {self.stard_date}, ending_date: {self.ending_date}, quantity: {self.quantity}, image: {self.image}"
    
# For GET request to http://localhost:5000/product
class GetProduct(Resource):
    def get(self):
        products= Product.query.all()
        prod_list = []
        for prod in products:
            una_fecha = prod.stard_date.strftime('%y/%m/%d')
            seg_fecha = prod.ending_date.strftime('%y/%m/%d')
            prod_data = {'id': prod.id, 'name': prod.name,'price': prod.price, 'stard_date': una_fecha, 'ending_date': seg_fecha, 'quantity': prod.quantity, 'image': prod.image}
            prod_list.append(prod_data)
        return {"products": prod_list}, 200

# For Post request to http://localhost:5000/product
class AddProduct(Resource):
    def post(self):
        if request.is_json:
            prod = Product(name=request.json['name'], price=request.json['price'],quantity=request.json['quantity'])
            db.session.add(prod)
            db.session.commit()
            # return a json response
            return make_response(jsonify({'id': prod.id, 'name': prod.name,'price': prod.price,'quantity': prod.quantity}), 201)
        else:
            return {'error': 'Request must be JSON'}, 400

# For put request to http://localhost:5000/product/?
class UpdateProduct(Resource):
    def put(self, id):
        if request.is_json:
            prod = Product.query.get(id)
            if prod is None:
                return {'error': 'not found'}, 404
            else:
                prod.name = request.json['name']
                prod.price = request.json['price']
                prod.quantity = request.json['quantity']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400

# For delete request to http://localhost:5000/product/?
class DeleteProduct(Resource):
    def delete(self, id):
        prod = Product.query.get(id)
        if prod is None:
            return {'error': 'not found'}, 404
        db.session.delete(prod)
        db.session.commit()
        return f'{id} is deleted', 200


api.add_resource(GetProduct, '/product')
api.add_resource(AddProduct, '/product')
api.add_resource(UpdateProduct, '/product/<int:id>')
api.add_resource(DeleteProduct, '/product/<int:id>')

#
# if __name__ == '__main__':
# app.run(debug=True)
#api.add_resource(Index, '/')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
#3401
#Probar con Curl o Postman
#POST
#curl --location --request POST 'http://localhost:5000/product' \
#--header 'Content-Type: application/json' \
#--data-raw '{  
#   "name": "tornillo",
#   "price": 10.20,
#   "quantity": 2
#}'

#UPDATE
#curl --location --request PUT 'http://localhost:5000/product/2' \
#--header 'Content-Type: application/json' \
#--data-raw '{
#            "id": 2,
#            "name": "tornillo",
#            "price": 10.20,
#            "quantity": 2
#        }'
        
#DELETE
#curl --location --request DELETE 'http://localhost:5000/product/1'
