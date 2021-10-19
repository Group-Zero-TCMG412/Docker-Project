from flask import Flask, jsonify
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
    while i < fib:
        n = fibArray[-1]+fibArray[-2]
        if n <= fib:
            fibArray.append(n)
        else:
            break
        i = n
    fibDict = {'Input': fib, 'Output': fibArray}
    return fibDict

@app.route('/is-prime/')
def prime_response():
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
    
    return "{num} is Prime: {resp}"
           
           
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
