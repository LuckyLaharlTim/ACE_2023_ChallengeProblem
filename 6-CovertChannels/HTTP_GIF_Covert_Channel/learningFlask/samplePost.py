import requests
import json

url = "http://127.0.0.1/index.php"

r = requests.post(url,files = {"q": "please request"})
data = r.json()

example = data["value1"]["value2"]

print(example)
