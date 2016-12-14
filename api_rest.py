#! /usr/bin/python3

import requests
import json
import struct
import base64

baseURL = 'http://localhost:8080/'
table = 'webpage'

headers = {
    "content-type":"text/xml"
}

body = bytes('<Scanner/>', 'utf-8')


print('PUT ' + baseURL + table + '/scanner')
a = requests.put(baseURL + table + '/scanner', body, headers=headers)

print('Satus code: ' + str(a.status_code) + ' ' + a.reason)
if a.status_code != 201:
    quit()

if 'Location' not in a.headers:
    print('Location header does not exist')
    quit()

scanURL = a.headers['Location']

headers = {
    "accept":"application/json",
}

print('GET ' + scanURL)
a = requests.get(scanURL, headers=headers)

print('Satus code: ' + str(a.status_code) + ' ' + a.reason)
if a.status_code != 200:
    quit()

#print(a.text)

def decode(s):
     data = base64.b64decode(s)
     try:
        n = struct.unpack("i", data)
        return str(n[0])
     except:
        try:
            return data.decode('utf-8')
        except:
            return str(data)

db = json.loads(a.text)
for row in db["Row"]:
    print(base64.b64decode(row["key"]))
    for cell in row["Cell"]:
        print("     " + decode(cell["column"]) + " : " + decode(cell["$"]))
        















