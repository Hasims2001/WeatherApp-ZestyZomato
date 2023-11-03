from app.WeatherApp import app
import pytest
import json
@pytest.fixture
def client():
    return app.test_client()


def test_welcome(client):
    response = client.get('/welcome')
    assert b'welcome to weather app!' in response.data

def test_weather_edge_case(client):
    response = client.get('/weather/City')
    response.status_code = 400
    assert b'City not found' in response.data

def test_weather(client):
    response = client.get('/weather/San%20Francisco')
    response.status_code = 200
    data = json.loads(response.data)
    assert 'City Data' == data['message']
    assert data['data']['weather'] in ['Cloudy', 'Sunny', 'Rainy', 'Hot']

def test_postWeather_edge_case(client):
    response = client.post('/weather', json={'city': 
    'Ahmedabad', 'temperature':34, 'weather': 'Cool'})
    data = json.loads(response.data.decode('utf-8'))
    assert 'Please write correct weather' == data['message']

def test_postWeather(client):
    response = client.post("/weather",  json={'city': "Ahemdabad", 'temperature': 34, 'weather': 'Sunny'})
    data = json.loads(response.data)
    assert 'Data added!' == data['message']


def test_putWeather_edge_case(client):
    response = client.put('/weather/Austin', json={'temperature':34, 'weather': 'Cool'})
    data = json.loads(response.data.decode('utf-8'))
    assert 'Invalid Data' == data['message']


def test_putWeather(client):
    response = client.put('/weather/Austin', json={'temperature':34, 'weather': 'Sunny'})
    data = json.loads(response.data.decode('utf-8'))
    assert 'Data updated!' == data['message']


def test_deleteWeather_edge_case(client):
    response = client.delete('/weather/InvalidCity')
    data = json.loads(response.data.decode('utf-8'))
    assert 'City not found' == data['message']

def test_deleteWeather(client):
    response = client.delete('/weather/Austin')
    data = json.loads(response.data.decode('utf-8'))
    assert 'Data deleted!' == data['message']