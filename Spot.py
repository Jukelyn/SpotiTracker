from dotenv import load_dotenv
load_dotenv()

import os
import requests

url = "https://accounts.spotify.com/api/token"

headers = {"Content-Type": "application/x-www-form-urlencoded"}

body = {
    "grant_type": "client_credentials",
    "client_id": os.getenv("CLIENT_ID"),
    "client_secret": os.getenv("CLIENT_SECRET")
}
requests.post(headers=headers, json=body)