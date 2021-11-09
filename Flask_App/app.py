from flask import Flask, redirect, url_for, request
import time

from redis.client import string_keys_to_dict
from flask_dance.contrib.slack import make_slack_blueprint, slack
import redis
import json
import math
from math import sqrt
#from redis import Redis, RedisError
import hashlib
# Connect to Redis

app = Flask(__name__)

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
    return 'Hello World! I have been seen {} times.\n'.format(count)
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
            return KeyDict
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
            return KeyDict
        else:
            redis_client.set(key, value)
            KeyDict = {'key': key, 'value': value, 'command': f'UPDATE {key}/{value}', 'result': True, 'error': 'None'}
            return KeyDict


@app.route("/keyval/<string>", methods=["GET", 'DELETE'])
def keyvalGETDELETE(string):
    if request.method == 'GET':
        if redis_client.exists(string) == 1:
            KeyDict = {'Key': string, 'value': redis_client.get(string), 'command': 'READ key/value pair', 'result': True, 'error': 'None'}
        else:
            KeyDict = {'Key': string, 'value': redis_client.get(string), 'command': 'READ key/value pair', 'result': False, 'error': 'key does not exist'}
        return KeyDict
        
    elif request.method == 'DELETE':
        if redis_client.exists(string) == 1:
            key = string
            KeyDict = {'Key': string, 'value': redis_client.get(string), 'command': f'DELETE {key}', 'result': True, 'error': 'None'}
            redis_client.delete(string)
            return KeyDict
        else:
            key = string
            KeyDict = {'Key': string, 'value': redis_client.get(string), 'command' : f'DELETE {key}', 'result': False, 'error': 'Unable to delete, key not found'}
            return KeyDict
    

@app.route("/md5/<string>", methods=["GET","POST"])
def md5(string):
    result = hashlib.md5(string.encode('utf-8')).hexdigest()
    hashData = {'Input':string,
            'Output':result}
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
                resp = 'False'
                break
            else:
                resp = 'True'
    elif num == 3:
        resp = 'True'
    else:
        resp = 'False'
    primeDict = {'input': num, 'output': resp}
    return primeDict

app.secret_key = "sekret"
blueprint = make_slack_blueprint(
    client_id = '73266387591.2668237953136',
    client_secret = '5c3ccd39c90315cd68ee69abde4969fc',
    scope=["identify", "chat:write:bot"],)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/slack-alert/<string>")
def slack_alert(string):
    slack_alert = string
    if not slack.authorized:
        return redirect(url_for("slack.login"))
    resp = slack.post("chat.postMessage", data={
        "channel": "#testing-day",
        "text": {slack_alert},
    })
    assert resp.ok, resp.text
    return f'true'
           
           
if __name__ == "__main__":
    app.run(debug ='true', host='0.0.0.0')
