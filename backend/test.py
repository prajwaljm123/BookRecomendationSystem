import requests

url = "http://127.0.0.1:5000/recommend"
data = {
    "interest": "science fiction",
    "rating": 4.0
}

response = requests.post(url, json=data)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)