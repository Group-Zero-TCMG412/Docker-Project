from flask import Flask
from markupsafe import escape
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

@app.route("/md5/<string>")
def md5(string):
    encoded = string.encode()
    result = hashlib.md5(encoded)
    return f'String {(string)} \n Encoded: {(result)}'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
