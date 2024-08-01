import json
from json.decoder import JSONDecodeError
from .default_config import default_config
from tool.tool import cover

try:
  f = open("config.json", "r", encoding = "utf8")
  user_config = json.loads(f.read())
  f.close()
except FileNotFoundError:
  user_config = {}
except JSONDecodeError:
  print("Error format of config.json")
  exit(-1)

base_config = {}
cover(base_config, default_config)
cover(base_config, user_config)