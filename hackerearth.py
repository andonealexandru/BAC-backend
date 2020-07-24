import requests

RUN_URL = u'http://api.hackerearth.com/v3/code/run/'
CLIENT_SECRET = '90cc525c23f99059c05da47bf9ea1de8d8a74304'

source = "print('SAL')"

data = {
    'client_secret': CLIENT_SECRET,
    'async': 0,
    'source': source,
    'lang': "PYTHON",
    'time_limit': 5,
    'memory_limit': 262144
}

r = requests.post(RUN_URL, data=data)
print(r.json())