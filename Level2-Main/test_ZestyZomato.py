import unittest
from ZestyZomato import app
from flask import Flask
import json

class ZomatoTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_welcome(self):
        response = self.app.get('/')
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Welcome to Zesty Zomato')
    
    # def test_dishes(self):
    #     # testing post and get
    #     newDish = {"name": "Panner Manchuriyan", "price": 450, "availability": "Yes", "store":"Ahemdabad, Gujarat"}
    #     response = self.app.post("/dishes", json=newDish)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['message'], 'dish added')

    #     response = self.app.get('/dishes')
    #     data = json.loads(response.data)
    #     self.assertEqual(data['message'], 'All Dishes') 
    
    # def test_dish(self):
    #     # testing put/patch, get, delete
    #     updateDish  = {"name": "Veg Moons", "price": 650, "availability": "Yes", "store":"Ahemdabad, Gujarat"}
    #     response = self.app.put("/dish/4", json=updateDish)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['message'], 'Dish with ID 4 has been updated')

    #     res = self.app.get('/dish/4')
    #     data = json.loads(res.data)
    #     self.assertEqual(data['message'], "Single Dish")
    #     self.assertEqual(data['Dish']['name'],  "Veg Moons")


    #     res = self.app.delete('/dish/4')
    #     data  = json.loads(res.data)
    #     self.assertEqual(data['message'], 'Dish with ID 4 has been deleted')


    # def test_edge_case(self):
    #     res = self.app.get('/dish/0')
    #     data = json.loads(res.data)
    #     self.assertEqual(data['message'], "Dish not found")


    # def test_orders(self):
    #   #testing post
    #     new_order ={
    #         "items" : [{"name":"Chicken Curry", "price": 450}, {"name":"Chicken Masala", "price": 550} ],
    #         "name" : "john",
    #         "email" : "john@gmail.com",
    #         "store" : "Wardha, Maharastra",
    #         "promocode" : "Flat5",
    #         "status" : "received"
    #         }
    #     res = self.app.post('/order', json=new_order)
    #     data = json.loads(res.data)
    #     self.assertEqual(data['message'], 'order added')
    #     self.assertEqual(data['order']['status'], 'received')

    def test_order(self):
        # testing get, patch, delete
        res = self.app.patch('/order/3', json={'name': "xyz"})
        data = json.loads(res.data)
        self.assertEqual(data['message'], f"Order with ID 3 has been updated")
        

        res = self.app.get('/order/3')
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Single Order')
        self.assertEqual(data['order']['name'], "xyz")
        

        res = self.app.delete('/order/3')
        data = json.loads(res.data)
        self.assertEqual(data['message'], "Order with ID 3 has been deleted")


        res = self.app.get('/order/3')
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Order not found')

if __name__ == '__main__':
    unittest.main()
