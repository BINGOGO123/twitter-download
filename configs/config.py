import json
from json.decoder import JSONDecodeError

try:
    f = open("headers.json", "rb")
    data = f.read()
    f.close()
except FileNotFoundError:
    print("headers.json is not exist")
    exit(-1)

try:
    content = data.decode("utf8")
except UnicodeDecodeError:
    print("headers.json can not be decoded with utf8")
    exit(-1)

try:
    headers = json.loads(content)
except JSONDecodeError:
    print("Error format of headers.json")
    exit(-1)
