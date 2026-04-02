import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert: GET /activities

def test_get_activities():
    # Arrange
    # (No setup needed, usamos el estado inicial)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Arrange-Act-Assert: POST /activities/{activity_name}/signup

def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Cleanup
    client.delete(f"/activities/{activity}/participant?email={email}")

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.delete(f"/activities/{activity}/participant?email={email}")

# Arrange-Act-Assert: DELETE /activities/{activity_name}/participant

def test_remove_participant_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser3@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

def test_remove_participant_not_found():
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

def test_signup_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "testuser4@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_remove_participant_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "testuser5@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
