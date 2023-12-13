from flask import Flask, request
import json
import time
app = Flask(__name__)

@app.route("/")
def index():
    return open('handskrift.html')

@app.route("/textract", methods=['POST'])
def textract_query():
    request_data = request.files['query']

    return json.dumps({'success': False})

@app.route("/textract/<number>", methods=['POST'])
def textract_persist(number):
    request_data = request.files['query']
    request_data.save(f'classification/{number}/{int(time.time())}.png')
    # with open(f'classification/{number}/{int(time.time())}.png', 'wb') as f:
    #     f.write(request_data)

    return json.dumps({'success': True})
