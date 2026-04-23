from fastapi.testclient import TestClient


def test_get_activities_returns_activity_dictionary(client: TestClient):
    # Arrange
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert payload

    for _activity_name, activity_data in payload.items():
        assert expected_fields.issubset(activity_data.keys())
        assert isinstance(activity_data["participants"], list)
        assert len(activity_data["participants"]) <= activity_data["max_participants"]
