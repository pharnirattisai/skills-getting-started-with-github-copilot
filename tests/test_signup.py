from urllib.parse import quote

from fastapi.testclient import TestClient

import src.app as app_module


def test_signup_adds_new_participant(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_returns_400_for_duplicate_participant(client: TestClient):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_returns_404_for_unknown_activity(client: TestClient):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_when_activity_is_full(client: TestClient):
    # Arrange
    activity_name = "Capacity Test"
    app_module.activities[activity_name] = {
        "description": "Capacity test activity",
        "schedule": "Fridays, 8:00 AM",
        "max_participants": 1,
        "participants": ["filled@mergington.edu"],
    }
    email = "next@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Activity is full"
    assert email not in app_module.activities[activity_name]["participants"]
