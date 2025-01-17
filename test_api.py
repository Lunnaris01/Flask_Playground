import requests

url = "http://127.0.0.1:5000/tasks"

response = requests.post(url, json={"title": "First Test"})

print("Status code: ", response.status_code)
print("Response json: ", response.json())
