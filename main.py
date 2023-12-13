from flask import Flask, request
import json
import time
import boto3
import base64

client = boto3.client('s3')

app = Flask(__name__)

@app.route("/")
def index():
    return open('handskrift.html')

@app.route("/textract/", methods=['POST'])
def textract_query():
    request_data = request.files['query']

    return json.dumps({'success': False})

@app.route("/textract/<number>", methods=['POST'])
def textract_persist(number):
    # prefix = 'data:image/jpeg;base64,'
    b64data = request.get_data().decode('ascii')[22:]
    bytes = base64.b64decode(b64data)
    # request_data = request.input_stream.read().decode('utf8')
    # print(request_data)
    # request_data.save(f'classification/{number}/{int(time.time())}.jpg')
    with open(f'classification/{number}/{int(time.time())}.jpg', 'wb') as f:
        f.write(bytes)

    return json.dumps({'success': True})
