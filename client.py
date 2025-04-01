import requests

server_url = "http://localhost:5000/message"
message_data = {"message": "Hello, Flask!"}

response = requests.post(server_url, json=message_data)
print("Server response:", response.json())
