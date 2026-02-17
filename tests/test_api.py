import pytest
import requests
import time


# Happy Path Test

def test_health_endpoint_returns_healthy(base_url):
    """Check if healthy endpoint returns healthy"""

    # Arrange
    response = requests.get(f"{base_url}/health")

    # Act
    assert response.status_code == 200
    assert response.json().get("status") == "healthy"


def test_get_all_events_endpoint_returns_events(base_url):
    """Check if events endpoint returns events"""
    # Arrange
    response = requests.get(f"{base_url}/events")

    # Act & Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_register_user_creates_new_user(base_url, user_data):
    """Check if new user creates new user"""

    # Act & Assert
    response = requests.post(f"{base_url}/auth/register", json=user_data)

    assert response.status_code == 201


def test_login_creates_jwl_token(base_url, user_data):
    """Check if login returns correct token"""

    # Arrange
    ## register new user
    requests.post(f"{base_url}/auth/register", json=user_data)

    ## login user
    response = requests.post(f"{base_url}/auth/login", json=user_data)

    # Act & Assert
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_create_public_event_requires_auth_and_succeeds_with_token(base_url, access_token):
    """Check if creates new event"""

    # Arrange
    event_data = {
        "title": "Test Event",
        "description": "Test the event endpoint",
        "date": "2026-02-18T16:00:00",
        "location": "Test Hub, Berlin",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }

    # create test event
    response = requests.post(
        f"{base_url}/events",
        json=event_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Act & Assert
    assert response.status_code == 201
    assert response.json()["title"] == "Test Event"
    assert response.json()["description"] == "Test the event endpoint"
    assert response.json()["date"] == "2026-02-18T16:00:00"
    assert response.json()["location"] == "Test Hub, Berlin"
    assert response.json()["capacity"] == 50
    assert response.json()["is_public"] is True
    assert response.json()["requires_admin"] is False


def test_attend_event(base_url, user_data):
    """Check if attend event"""

    # Arrange
    response = requests.post(f"{base_url}/rsvps/event/1", json=user_data)

    assert response.status_code == 201



# Error/Edge Cases

def test_register_user_two_times(base_url, user_data):
    """Check if user can register two times"""

    # Arrange
    requests.post(f"{base_url}/auth/register", json=user_data)
    response = requests.post(f"{base_url}/auth/register", json=user_data)

    # Assert
    assert response.status_code == 400
    assert "Username already exists" in response.json().get("error")


def test_create_public_event_requires_auth_and_fails_without_token(base_url):
    """Check if creates new event"""

    # Arrange
    event_data = {
        "title": "Test Event",
        "description": "Test the event endpoint",
        "date": "2026-02-18T16:00:00",
        "location": "Test Hub, Berlin",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }

    # create test event
    response = requests.post(
        f"{base_url}/events",
        json=event_data
    )

    # Assert
    assert response.status_code == 401


def test_attend_private_event(base_url, access_token, user_data):
    """Try to attend a private event without auth"""

    # Arrange
    ## create private event
    event_data = {
        "title": "Test Event",
        "description": "Test the event endpoint",
        "date": "2026-02-18T16:00:00",
        "location": "Test Hub, Berlin",
        "capacity": 50,
        "is_public": False,
        "requires_admin": False
    }

    ## create private test event
    response = requests.post(
        f"{base_url}/events",
        json=event_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    ## get event id
    event_id = response.json()["id"]

    ## try to get private event
    response_get_event = requests.post(f"{base_url}/rsvps/event/{event_id}", json=user_data)


    # Assert
    assert response.status_code == 201
    assert response_get_event.status_code == 401
    assert "Authentication required for this event" in response_get_event.json().get("error")