import requests
from dotenv import load_dotenv
import os

load_dotenv()

webhook_url = os.getenv("API-KEY-CDC")


url = "http://localhost:5678/webhook-test/test-logiciel-cdc"
headers = {
    "Content-Type": "application/json",
    "API-KEY-CDC": webhook_url,
}
json = {
    "id": "1234",
}

if __name__ == "__main__":
    x = requests.post(url, headers=headers, json=json)
    print(x.status_code)
    print("Hello, World!")