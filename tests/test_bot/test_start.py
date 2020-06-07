import requests
import json
import os

from app import settings


APP_HOST = 'http://localhost'
APP_PORT = '5000'


# def test_start_handler():
#     request_path = os.path.dirname(os.path.abspath(__file__)) + '/request.json'
#     with open(request_path, 'r') as file:
#         requests.post(f"{APP_HOST}:{APP_PORT}/secret", json=json.load(file))
