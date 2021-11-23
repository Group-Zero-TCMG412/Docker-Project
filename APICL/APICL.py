
import requests
import click
import json


@click.group()
def cli():
    """Command Line tool to access group zero's API.
    
    Description and usage of commands:
    
    md5 -> Entering this command will send a get request to the /md5/ endpoint. This endpoint expects a input and will return the hashdata for that input.


    fibonacci -> Entering this command will send a get request to the /fibonacci/ endpoint. This endpoint expects a input and will return the fibonacci output for that input.


    factorial -> Entering this command will send a get request to the /factorial/ endpoint. This endpoint expects a input and will return the factorial output for that input.


    isprime -> Entering this command will send a get request to the /isprime/ endpoint. This endpoint expects a input and will see if the given input is prime or not.


    KEYVAL commands:


    keyvalsend -> Entering this commanding will send a post request to /keyval/ endpoint. This command will execute a function that will ask the user for two inputs: key and value. It will then also ask the user for a url.


    keyvalupdate -> Entering this commanding will send a put request to /keyval/ endpoint. This command will execute a function that will ask the user for two inputs: key and value. It will then also ask the user for a url.


    keyvalget -> Entering this commanding will send a get request to /keyval/ endpoint. This command will execute a function that will ask the user for one input as well as a url.


    keyvaldelte -> Entering this commanding will send a delete request to /keyval/ endpoint.  This command will execute a function that will ask the user for one input as well as a url.
    """
    pass


@cli.command()
@click.argument('var')
def md5(var):
    r = requests.get('http://localhost:80/md5/{}'.format(var)).json()
    print('input: {}, output: {}'.format(r['input'], r['output']))

@cli.command()
@click.argument('var')
def fibonacci(var):
    r = requests.get('http://localhost:80/fibonacci/{}'.format(var)).json()
    print('input: {}, output: {}'.format(r['input'], r['output']))

@cli.command()
@click.argument('var')
def factorial(var):
    r = requests.get('http://localhost:80/factorial/{}'.format(var)).json()
    print('input: {}, output: {}'.format(r['input'], r['output']))


@cli.command()
@click.argument('var')
def isprime(var):
    r = requests.get('http://localhost:80/is-prime/{}'.format(var)).json()
    print('input: {}, output: {}'.format(r['input'], r['output']))



@cli.command()
def keyvalsend():
    key = input('Key: ')
    value = input('Value: ')
    url = input('Url: ')
    data = {'key': key, 'value': value}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.text)



@cli.command()
def keyvalupdate():
    key = input('Key: ')
    value = input('Value: ')
    url = input('Url: ')
    data = {'key': key, 'value': value}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(r.text)

@cli.command()
def keyvalget():
    key = input('Key: ')
    url = input('Url: ')
    data = {'key': key}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.get(url, data=json.dumps(data), headers=headers)
    print(r.text)



@cli.command()
def keyvaldelete():
    key = input('Key: ')
    url = input('Url: ')
    data = {'key': key}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.delete(url, data=json.dumps(data), headers=headers)
    print(r.text)

