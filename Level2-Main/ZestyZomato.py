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

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items= db.Column(db.String(500), nullable=False)
    totalBill= db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    store = db.Column(db.String(255), nullable=False)
    promocode = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    
    def __init__(self,items, totalBill, name, email, date,store, promocode, status): 
        self.items = items
        self.totalBill = totalBill
        self.name = name
        self.email = email
        self.date = date
        self.store = store
        self.promocode = promocode  
        self.status = status  


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
    # dish = Dishes.query.get(dish_id)
    dish = db.session.get(Dishes, dish_id)
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


@app.route('/order', methods=['GET','POST'])
def orders():
    if(request.method == "POST"):
        data = request.get_json()
        try:
            total = 0
            items = ""
            orders = data['items']
            
            for i in orders:
                items += i['name'] + ", "
                total += i['price']
            temp = datetime.date.today()
            today = temp.strftime('%d/%m/%y')
            
            if(data['promocode'] == 'FLAT5'):
                total = (total*5)/100
            new_order = Orders(items=items, totalBill=total, name=data['name'], email=data['email'], date=today,store=data['store'], promocode=data['promocode'], status=data['status'])

            db.session.add(new_order)
            db.session.commit()
            return jsonify({'message': "order added", 'order': {"items":items, "totalBill":total, "name":data['name'], "email":data['email'], "date":today,"store":data['store'], "promocode":data['promocode'], "status":data['status']}})
        except:
            return jsonify({'message': "something is wrong"})


     # Get request    
    allOrders = Orders.query.all()
    order_list = []

    for order in allOrders:
        order_info = {
            'id': order.id,
            "items" : order.items,
            "totalBill" : order.totalBill,
            "name" : order.name,
            "email" : order.email,
            "date" : order.date,
            "store" : order.store,
            "promocode" : order.promocode  ,
            "status" : order.status  ,
        }
        order_list.append(order_info)

    return jsonify({'message': "All orders", "orders": order_list})


@app.route('/order/<int:id>', methods=['GET', 'PUT', "PATCH", "DELETE"])
def paramOrders(id):
    order = db.session.get(Orders, id)
    if(order):
        if(request.method == 'GET'):
            order_dict = {
                'id': order.id,
                'items': order.items,
                "totalBill" : order.totalBill,
                "name" : order.name,
                "email" : order.email,
                "date" : order.date,
                "store" : order.store,
                "promocode" : order.promocode  ,
                "status" : order.status  ,

            }
            return jsonify({'message': "Single Order", "order": order_dict})
        
        if(request.method == 'DELETE'):
            db.session.delete(order)
            db.session.commit()
            return jsonify({'message': f'Order with ID {id} has been deleted'})
        
         
        data = request.get_json()
        data_json = json.dumps(data)
        data_dict = json.loads(data_json)
       
        if 'items' in data_dict:
            items = ""
            for i in data_dict['items']:
                items += i['name'] + ", "
            order.items = items
        if 'totalBill' in data_dict:
            order.totalBill = data_dict['totalBill']
        if 'email' in data_dict:
            order.email = data_dict['email']
        if 'name' in data_dict:
            order.name = data_dict['name']
        if 'date' in data_dict:
            order.date = data_dict['date']
        if 'store' in data_dict:
            order.store = data_dict['store']
        if 'promocode' in data_dict:
            order.promocode = data_dict['promocode']
        if 'status' in data_dict:
            order.status = data_dict['status']
        db.session.commit()
        return jsonify({'message': f'Order with ID {id} has been updated'})
    else:
        return jsonify({'message': 'Order not found'}) 

if __name__ == '__main__':
    app.run(debug=True)
