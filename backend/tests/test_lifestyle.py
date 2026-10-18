def test_lifestyle_assessment_calculation(client, auth_headers_user1):
    # Healthy lifestyle habits (choice 4 = lowest risk)
    payload = {
        "activity": 4,
        "diet": 4,
        "smoking": 4,
        "alcohol": 4,
        "sleep": 4,
        "stress": 4,
        "weight": 4,
    }
    res = client.post(
        "/api/v1/lifestyle-assessments",
        json=payload,
        headers=auth_headers_user1,
    )
    assert res.status_code == 201
    data = res.get_json()["data"]
    assert data["category"] == "lower"
    assert data["score"] == 0.0
    assert len(data["breakdown"]) == 7
    assert "disclaimer" in data


def test_lifestyle_assessment_higher_risk(client):
    # High risk lifestyle habits (choice 1 = highest risk)
    payload = {
        "activity": 1,
        "diet": 1,
        "smoking": 1,
        "alcohol": 1,
        "sleep": 1,
        "stress": 1,
        "weight": 1,
    }
    res = client.post(
        "/api/v1/lifestyle-assessments",
        json=payload,
    )
    assert res.status_code == 201
    data = res.get_json()["data"]
    assert data["category"] == "higher"
    assert data["score"] == 100.0
    assert len(data["recommendations"]) > 0


def test_lifestyle_invalid_input(client):
    res = client.post(
        "/api/v1/lifestyle-assessments",
        json={"activity": 99},  # Invalid choice
    )
    assert res.status_code == 422
