import json

with open('payload.json', 'r') as f:
    payload = f.read()

from handler.handler import lambda_handler

print(lambda_handler(json.loads(payload), None))