import pytest
import time
import json

import requests

BASE_URL = "http://127.0.0.1:5000/api"

@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def user_data():
    """create and return user data (username, password)"""
    time_stamp = int(time.time())
    username = f"username_{time_stamp}"

    user_data = {
        "username": username,
        "password": "UserPass123",
    }

    return user_data


@pytest.fixture
def access_token(base_url, user_data):
    """
    - take in user data,
    - register a new user,
    - login and return access token
    """
    # register new user
    requests.post(f"{base_url}/auth/register", json=user_data)

    # login user
    response = requests.post(f"{base_url}/auth/login", json=user_data)


    # return access_token
    return response.json()["access_token"]