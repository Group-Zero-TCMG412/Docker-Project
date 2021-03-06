from flask import Flask, redirect, url_for, request, Response
import time
import requests
from flask.helpers import make_response
from redis.client import string_keys_to_dict
from cryptography.fernet import Fernet
import redis
import json
import math
from math import sqrt
import hashlib


app = Flask(__name__)

# dadaw 

redis_client = redis.Redis(host='redis', port='6379', charset="utf-8", decode_responses=True)

def get_hit_count():
    retries = 5
    while True:
        try:
            return redis_client.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)



@app.route("/count")
def index():
    count = get_hit_count()
    return json.dumps(True)
@app.route('/user/<username>')
def show_user(username):
    return f'User {(username)}'
@app.route("/hello")
def hello():
    return "Hello, World"


@app.route("/keyval", methods=['POST', 'PUT'])
def keyvalPUTPOST():
    KeyDict = {}
    if request.method == 'POST':
        KeyPair = request.get_json()
        key = KeyPair['key']
        value = KeyPair['value']
        if redis_client.exists(key) == 1:
            KeyDict = {"key": key, "value": value,"command": f"CREATE {key}/{value}","result": False, "error": "Unable to add pair: key already exists"}
            return Response(json.dumps(KeyDict)), 409
            
        else:
            redis_client.set(key, value)
            KeyDict = {'key': key, 'value': value, 'command': f"CREATE {key}/{value}", 'result': True, 'error': 'None'}
            return KeyDict
    elif request.method == 'PUT':
        KeyPair = request.get_json()
        key = KeyPair['key']
        value = KeyPair['value']
        if redis_client.exists(key) == 0:
            KeyDict = {'key': key, 'value': value, 'command': f'UPDATE {key}/{value}', 'result': False, 'error': 'Unable to update: key does not exist'}
            return Response(json.dumps(KeyDict)), 409
        else:
            redis_client.set(key, value)
            KeyDict = {'key': key, 'value': value, 'command': f'UPDATE {key}/{value}', 'result': True, 'error': 'None'}
            return KeyDict


@app.route("/keyval/<string>", methods=["GET", 'DELETE'])
def keyvalGETDELETE(string):
    if request.method == 'GET':
        if redis_client.exists(string) == 1:
            KeyDict = {'Key': string, 'value': redis_client.get(string), 'command': 'READ key/value pair', 'result': True, 'error': 'None'}
            return KeyDict
        else:
            #resp = Flask.Response(status=409)
            KeyDict = {'Key': string, 'value': redis_client.get(string), 'command': 'READ key/value pair', 'result': False, 'error': 'key does not exist'}
            return Response(json.dumps(KeyDict)), 409
        
    elif request.method == 'DELETE':
        if redis_client.exists(string) == 1:
            key = string
            KeyDict = {'Key': string, 'value': redis_client.get(string), 'command': f'DELETE {key}', 'result': True, 'error': 'None'}
            redis_client.delete(string)
            return KeyDict
        else:
            key = string
            #resp = Flask.Response(status=409)
            KeyDict = {'Key': string, 'value': redis_client.get(string), 'command' : f'DELETE {key}', 'result': False, 'error': 'Unable to delete, key not found'}
            return Response(json.dumps(KeyDict)), 409
    

@app.route("/md5/<string>")
def md5(string):
    result = hashlib.md5(string.encode('utf-8')).hexdigest()
    hashData = {'input':string,
            'output':result}
    #hashjson = json.dumps(hashData)
    #print(hashjson)
    return hashData


@app.route("/factorial/<int:factor>")
def factorial(factor):
    i = factor
    product = 0
    if factor<0:
        return 'Error, can not factor negative number.'
    else:
        product = math.factorial(factor)
    factorialDict = {'input':factor, 'output': product}
    return factorialDict
@app.route("/fibonacci/<int:fib>")
def fibonacci(fib):
    fibArray = [0,1,1]
    i = 1
    if fib < 0:
        return 'Error, must input a positive integer.'
    else:
        while i < fib:
            n = fibArray[-1]+fibArray[-2]
            if n <= fib:
                fibArray.append(n)
            else:
                break
            i = n
    fibDict = {'input': fib, 'output': fibArray}
    return fibDict

@app.route('/is-prime/<int:num>')
def prime_response(num):
    if num > 3:
        for n in range(2, int(sqrt(num))+1):
            if (num % n) == 0:
                resp = False
                break
            else:
                resp = True
    elif num == 3:
        resp = True
    else:
        resp = False
    primeDict = {'input': num, 'output': resp}
    return primeDict



@app.route("/slack-alert/<string>")
def slack_alert(string):
    key = b'fYJNS-io_ZkOD1WsuNtkZ60YydwyRU2dgiY8XH5mB40='
    f = Fernet(key)
    Token = b'gAAAAABhnQJ40STu8arPPZAiLfuGE9CgVGS4AMfZNv7aL2-GM0ctYqvbxXhKw0gSky4JoICTLcJm5tP6g09C6QrwQOIcu48OIg5Pzvtm_BtJtj-Ia9fVYiWnRNSvsrBISKC55wiaw0RKC5CmsFVv12C3m15US6EJIQ=='
    slack_token = f.decrypt(Token)
    data = {
    'token': slack_token,
    'channel': '#testing-day',    # User ID. 
    'as_user': True,
    'text': string
}
    r = requests.post(url='https://slack.com/api/chat.postMessage',
              data=data)
    if r.status_code == 404:
        output = False
    else:
        output = True
    slackdict = {'input': string, 'output': output}
    print(slackdict)
    return slackdict
           
           
if __name__ == "__main__":
    app.run(debug ='true', host='0.0.0.0')
