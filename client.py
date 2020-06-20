import json

import requests


def get_inventory_details():
    uri = 'http://localhost:1234/api/inventory'
    return requests.get(uri).json()


def rabbit():
    uri = 'http://localhost:1234/rabbitmq/producer'
    payload = {'empId': '1', 'empName': 'Ashish'}
    headers = {'Content-type': 'application/json'}
    return requests.get(uri, params=payload, headers=headers).json()


def save_inventory_details():
    uri = 'http://localhost:1234/api/inventory'
    payload = {"productName": "Laptops", "locationName": "Bangalore", "quantity": 1000}
    headers = {'Content-type': 'application/json'}
    return requests.post(uri, data=json.dumps(payload), headers=headers).json()
