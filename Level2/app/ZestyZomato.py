from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
import json
import datetime
import random

app = Flask(__name__)
app.secret_key = 'secret'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ZestyZomato.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Dishes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.String(10), nullable=False)
    store =  db.Column(db.String(10), nullable=False)
    def __init__(self, name, price, availability, store): 
        self.name = name
        self.price = price
        self.availability = availability  
        self.store = store


with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def welcome():
    return jsonify({'message': "Welcome to Zesty Zomato"})

@app.route("/dishes", methods=['GET', "POST"])
def dishes():
    # post request
    if(request.method == 'POST'):
        dish = request.get_json()
        if(dish['name'] and dish['price'] and dish['availability'] and dish['store']):
            new_dish = Dishes(name=dish['name'], price=dish['price'], availability=dish['availability'], store=dish['store'])
            db.session.add(new_dish)
            db.session.commit()

            return jsonify({'message': "dish added"})


    # Get request
    allDishes = Dishes.query.all()
    dishes_list = []

    for dish in allDishes:
        dish_info = {
            'id': dish.id,
            'name': dish.name,
            'price': dish.price,
            'availability': dish.availability,
            'store': dish.store
        }
        dishes_list.append(dish_info)

    return jsonify({'message': "All Dishes", "Dishes": dishes_list})


@app.route("/dish/<int:dish_id>", methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def paramDishes(dish_id):
    # dish = Dishes.query.filter_by(id=1).first()
    # dish = Dishes.query.get(1)
    # dish = db.session.get(Dishes, 1)
    dish = db.session.execute(db.select(Dishes).filter_by(id=1)).scalar()
    print(dish)
    if(dish):
        if(request.method == 'GET'):
            dish_dict = {
                'id': dish.id,
                'name': dish.name,
                'price': dish.price,
                'availability': dish.availability,
                'store': dish.store
            }

            return jsonify({'message': 'Single Dish', 'Dish': dish_dict})
        
        if(request.method == 'DELETE'):
            db.session.delete(dish)
            db.session.commit()
            return jsonify({'message': f'Dish with ID {dish_id} has been deleted'})
        
        data = request.get_json()
        if 'name' in data:
            dish.name = data['name']
        if 'price' in data:
            dish.price = data['price']
        if 'availability' in data:
            dish.availability = data['availability']
        if 'store' in data:
            dish.store = data['store']
        db.session.commit()
        return jsonify({'message': f'Dish with ID {dish_id} has been updated'})
    else:
        return jsonify({'message': 'Dish not found'}) 



if __name__ == '__main__':
    app.run(debug=True)
