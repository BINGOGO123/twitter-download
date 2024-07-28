import json

f = open("headers.json", "rb")
headers = json.loads(f.read().decode("utf8"))
f.close()
