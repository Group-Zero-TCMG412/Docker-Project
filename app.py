from flask import Flask, redirect, url_for
from flask_dance.contrib.slack import make_slack_blueprint, slack
import json
import math
from math import sqrt
#from redis import Redis, RedisError
import hashlib
# Connect to Redis

app = Flask(__name__)




@app.route("/")
def index():
    return "Index Page"
@app.route('/user/<username>')
def show_user(username):
    return f'User {(username)}'
@app.route("/hello")
def hello():
    return "Hello, World"

@app.route("/md5/<string>", methods=["GET","POST"])
def md5(string):
    result = hashlib.md5(string.encode('utf-8')).hexdigest()
    hashData = {'input':string,
            'output':result}
    hashjson = json.dumps(hashData)
    print(hashjson)
    return hashjson


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
    return f true
           
           
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
