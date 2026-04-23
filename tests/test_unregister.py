from urllib.parse import quote

from fastapi.testclient import TestClient

import src.app as app_module


def test_unregister_removes_existing_participant(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/unregister", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client: TestClient):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/unregister", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_returns_404_for_unknown_participant(client: TestClient):
    # Arrange
    activity_name = "Debate Team"
    email = "not.registered@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/unregister", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Participant not found in this activity"


def test_unregister_removes_all_duplicate_participant_entries(client: TestClient):
    # Arrange
    activity_name = "Science Club"
    email = "duplicate@mergington.edu"
    app_module.activities[activity_name]["participants"].extend([email, email])
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
