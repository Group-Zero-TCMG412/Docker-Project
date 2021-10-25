from flask import Flask, redirect, url_for
from flask_dance.contrib.slack import make_slack_blueprint, slack
import json
import math
#from redis import Redis, RedisError
import hashlib
import os
import socket
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
    hashData = {'Input':string,
            'Output':result}
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
    factorialDict = {'Input':factor, 'Output': product}
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
    fibDict = {'Input': fib, 'Output': fibArray}
    return fibDict

@app.route('/is-prime/<int:num>')
def prime_response(num):
    num = int(input('Input: '))
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                resp = False
                break
            else:
                resp = True
    else:
        resp = False
    primeDict = {'Num': num, 'Output': resp}
    return primeDict

app.secret_key = "sekret"
blueprint = make_slack_blueprint(
    client_id="73266387591.2634598506870",
    client_secret="410fba6fdc6db953b8bc7385399b8144",
    scope=["identify", "chat:write:bot"],
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/slack-alert/<string>")
def slack_alert(string):
    slack_alert = input("What do you want to say:\n")
    if not slack.authorized:
        return redirect(url_for("slack.login"))
    resp = slack.post("chat.postMessage", data={
        "channel": "#zer0",
        "text": {slack_alert},
    })
    assert resp.json()["ok"], resp.text
    return 'I just said ',{slack_alert},' in the #zer0 channel!'
           
           
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
