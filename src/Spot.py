"""
Basic modules.
"""
import os  # for .env interactions
import base64  # For encoding
import json  # For parsing API data
import requests  # For API usage
from dotenv import load_dotenv
load_dotenv()  # For .env usage


def to_dict(response) -> dict:
    '''API reponse to dictionary'''
    return json.loads(json.dumps(response.json()))


def get_access_token() -> str:
    '''Gets the access token to use the Spotify API'''

    url = "https://accounts.spotify.com/api/token"

    auth_string = f'{os.getenv("CLIENT_ID")}:{os.getenv("CLIENT_SECRET")}'
    auth_string = auth_string.encode("utf-8")
    encoded = base64.b64encode(auth_string)

    headers = {
        "Authorization": "Basic " + str(encoded, "utf-8"),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    body = {
        "grant_type": "client_credentials"
    }

    # Passing info to Spotify for the API Access Token
    response = requests.post(url=url, headers=headers, data=body, timeout=10)
    response_as_dict = to_dict(response)
    # This is only valid for 1hr at a time
    access_token = response_as_dict["access_token"]
    print(access_token)
    return access_token


token = get_access_token()
# print("Access token renewed...")


def refresh_token():
    """
    Refershes the API token
    """
    # TODO: Find out how to refresh the damn token.
    url = "https://accounts.spotify.com/api/token"

    access_token = get_access_token()

    auth_string = f'{os.getenv("CLIENT_ID")}:{os.getenv("CLIENT_SECRET")}'
    auth_string = auth_string.encode("utf-8")
    encoded = base64.b64encode(auth_string)

    headers = {
        "Authorization": "Basic " + str(encoded, "utf-8"),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    body = {
        "grant_type": "refresh_token",
        "refresh_token": access_token
    }

    response = requests.post(url=url, headers=headers, data=body, timeout=10)
    response_as_dict = to_dict(response)
    print(response_as_dict)


refresh_token()


def get_header():
    """
    API Header maker
    """
    return {"Authorization": "Bearer " + token}


def get_user_id() -> str:
    '''Gets the current user's user_id'''
    # https://api.spotify.com/v1/me

    url = "https://api.spotify.com/v1/me"

    response = requests.get(url=url, headers=get_header(), timeout=10)
    response = to_dict(response)
    if not response["error"]:
        user_id = response["display_name"]
        # print(user_id)
        return user_id
    else:
        msg = f"ERROR BADDDDD AHHHH. Status: {response['error']['status']:}\n"
        msg += "Bad or expired token. This can happen if the user revoked a "
        msg += "token or the access token has expired. You should re-authenti"
        msg += "cate the user."
        # Surely there is a normal way to do this lol... oh well, if it ain't
        # broken, don't fix it
        print(msg)
        os._exit(11)


def get_user_profile() -> str:
    '''Gets a user profile using the user_id of that user.'''

    # https://api.spotify.com/v1/users/{user_id}
    url = "https://api.spotify.com/v1/users/"

    response = requests.get(
        url=f"{url}{get_user_id()}", headers=get_header(), timeout=10
    )

    return response.text


user_profile = get_user_profile()
print(user_profile)
