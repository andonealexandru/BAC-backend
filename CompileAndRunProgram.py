import requests

RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
CLIENT_SECRET = '90cc525c23f99059c05da47bf9ea1de8d8a74304'
source = ""


def init_source_input():
    with open("test_main.txt", "r") as code_file:
        source_code = code_file.read()
    with open("input.txt", "r") as input_file:
        input = input_file.read()
    return source_code, input

def send_request(lang_comp):
    source, input = init_source_input()

    print('Got source: ' + source)
    data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': source,
        'input': input,
        'lang': lang_comp,
        'time_limit': 5,
        'memory_limit': 262144,
    }

    r = requests.post(RUN_URL, data=data)
    print(r.json())

send_request("CPP11")