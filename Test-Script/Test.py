import requests

import sys

import yaml
import json
from colorama import Fore


def print_list_item(list):
    if len(list) > 1:
        return list
    else:
        return list[0]
def check_json(json, keyval=False):
    try:
        if keyval == True:
            if 'key' in json and 'value' in json and 'command' in json and 'result' in json and 'error' in json:
                return False, json.get('result')
            else:
                return True, json.get('result', None)
        else:
            if 'input' in json and 'output' in json:
                return False, json.get('output')
            else:
                return True, json.get('output', None)
    except:
        return True, None
PASSED = 0
FAILED = 0

location = 'localhost:5000'
for t in yaml.full_load(open('test.yaml')):
    ENDPOINT = t['url']
    URL = 'http://'+ location + ENDPOINT
    METHOD = t['method']
    EXP_RESULT = t['result']
    STATUS = t['status_codes']

    INVALID_PAYLOAD = None
    JSON_RESULT = None

    if METHOD == 'GET':
        resp = requests.get(URL)
    if METHOD == 'POST':
        data = {'key': t['key_key'], 'value': t['key_val']}
        resp = requests.post(URL, json=data)
    if METHOD == 'DELETE':
        resp = requests.delete(URL)
    if METHOD == 'PUT':
        data = {'key': t['key_key'], 'value': t['key_val']}
        resp = requests.put(URL, json=data)


    E_PAD = '... '.ljust(33-len(ENDPOINT[:28]))
    M_PAD = ' '.ljust(7-len(METHOD))
    print(Fore.WHITE + f'Method  {METHOD}{M_PAD}{ENDPOINT[:28]} {E_PAD}', end='')

    try:
        raw_json = resp.json()
    except:
        raw_json = None
    keyval = True if ENDPOINT[:7] == '/keyval' else False
    INVALID_PAYLOAD, JSON_RESULT = check_json(raw_json, keyval)

    if resp.status_code in STATUS:

        if JSON_RESULT == EXP_RESULT or EXP_RESULT == None:
            print(u"\u2705 " + Fore.GREEN + "PASSED"+ Fore.WHITE)

            PASSED +=1
        elif INVALID_PAYLOAD:
            print(u'\u274c ' + Fore.RED +  'FAILED'+ Fore.WHITE)
            print(Fore.WHITE + f'    - INVALID JSON RESPONSE')
            print(Fore.WHITE + f"    - JSON DATA {resp.json()}")
            FAILED +=1
        else:
            print(Fore.WHITE + u'\u274c ' + Fore.RED +  'FAILED'+ Fore.WHITE)
            print(f"    - EXPECTED output: '{str(EXP_RESULT)}")
            print(f"    - ACTUAL output: '{str(JSON_RESULT)}")
            FAILED +=1
    else:
        print(u'\u274c ' + Fore.RED +  'FAILED'+ Fore.WHITE)
        print(Fore.WHITE + f"    - EXPECTED HTTP STATUS CODE: '{print_list_item(STATUS)}")
        print(Fore.WHITE + f"    - ACTUAL HTTP Status: '{resp.status_code}")
        print(Fore.WHITE + f"    - JSON DATA {resp.json()}")

        FAILED+=1
sys.exit(FAILED)