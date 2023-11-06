from app.ZestyZomato import app
import pytest
import json

@pytest.fixture
def client():
    return app.test_client()

def test_welcome(client):
    response = client.get('/')
    data = json.loads(response.data)
    assert 'Welcome to Zesty Zomato' == data['message']


def test_getDishes(client):
    response = client.get('/dishes')
    data = json.loads(response.data)
    print('all', data)
    assert 'All Dishes' == data['message']

def test_Dishes_edge_case(client):
    Single_Dish = client.get('/dish/0')
    single = json.loads(Single_Dish.data)
    assert 'Dish not found' == single['message']

    Single_Dish = client.put('/dish/0')
    single = json.loads(Single_Dish.data)
    assert 'Dish not found' == single['message']

    Single_Dish = client.delete('/dish/0')
    single = json.loads(Single_Dish.data)
    assert 'Dish not found' == single['message']

def test_get_single_dish(client):
    response = client.get('/dish/1')
    data = json.loads(response.data)
    assert 'Single Dish' == data['message']

