#import json
from flask import Flask,jsonify,request,Response,make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://admin:admin@localhost:3306/devops'

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__="pyproducts"
    productId = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(40))
    description = db.Column(db.String(40))
    productCode = db.Column(db.String(40))
    price = db.Column(db.Float)
    starRating = db.Column(db.Float)
    imageurl = db.Column(db.String(40))
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def _init_(self,productName,description,productCode,price,starRating,imageurl):
        self.productName = productName
        self.description = description
        self.productCode= productCode
        self.price = price
        self.starRating = starRating
        self.imageurl = imageurl
    
    def _repr_(self):
        return "%self.productId"
    
db.create_all()
class ProductSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model =Product
        sqla_session=db.session
    productId=fields.Number(dump_only=True)
    productName=fields.String(required=True)
    description=fields.String(required=True)
    productCode=fields.String(required=True)
    price=fields.Number(required=True)
    starRating=fields.Number(required=True)
    imageurl=fields.String(required=True)

@app.route('/products',methods=['POST'])    
def createProduct():
    data=request.get_json()
    product_schema=ProductSchema()
    product=product_schema.load(data)
    result=product_schema.dump(product.create())
    return make_response(jsonify({'product':result}),201)
@app.route('/products',methods=['GET'])    
def getAllProducts():
    get_products=Product.query.all()
    productSchema=ProductSchema(many=True)
    products=productSchema.dump(get_products)
    return make_response(jsonify({'products':products}))

@app.route('/products/<int:productId>',methods=['GET'])    
def getProductById(productId):
    get_products=Product.query.get(productId)
    productSchema=ProductSchema()
    products=productSchema.dump(get_products)
    return make_response(jsonify({'products':products}))

@app.route('/products/<int:productId>',methods=['DELETE'])    
def deleteProductById(productId):
    get_products=Product.query.get(productId)
    db.session.delete(get_products)
    db.session.commit()
    return make_response(jsonify({'products':'product deleted'}))

@app.route('/products/<int:productId>',methods=['PUT'])    
def updateProductById(productId):
    data=request.get_json()
    get_products=Product.query.get(productId)
    if data.get('price'):
        get_products.price=data['price']
    db.session.add(get_products)
    db.session.commit()
    productSchema=ProductSchema(only=['productId','price'])
    products=productSchema.dump(get_products)
    return make_response(jsonify({'products':products}),200)

@app.route('/products/find/<productName>',methods=['GET'])    
def getProductByname(productName):
    get_products=Product.query.filter_by(productName=productName)
    productSchema=ProductSchema(many=True)
    products=productSchema.dump(get_products)
    return make_response(jsonify({'products':products}),200)

app.run(port=4005)
