from tests.test_predictions import VALID_PATIENT_FEATURES


def test_combined_assessments_history(client, auth_headers_user1):
    # Add 1 heart prediction
    client.post("/api/v1/predictions/heart", json={"features": VALID_PATIENT_FEATURES}, headers=auth_headers_user1)

    # Add 1 lifestyle assessment
    client.post(
        "/api/v1/lifestyle-assessments",
        json={"activity": 3, "diet": 3, "smoking": 4, "alcohol": 3, "sleep": 3, "stress": 2, "weight": 3},
        headers=auth_headers_user1,
    )

    # Get combined history
    all_res = client.get("/api/v1/assessments/history?type=all", headers=auth_headers_user1)
    assert all_res.status_code == 200
    items = all_res.get_json()["data"]["items"]
    assert len(items) == 2

    # Filter heart only
    heart_res = client.get("/api/v1/assessments/history?type=heart", headers=auth_headers_user1)
    assert heart_res.status_code == 200
    heart_items = heart_res.get_json()["data"]["items"]
    assert len(heart_items) == 1
    assert heart_items[0]["type"] == "heart"

    # Toggle hospital summary inclusion
    rec_id = heart_items[0]["id"]
    patch_res = client.patch(
        f"/api/v1/assessments/{rec_id}/hospital-summary",
        json={"include_in_hospital_summary": False},
        headers=auth_headers_user1,
    )
    assert patch_res.status_code == 200
    assert patch_res.get_json()["data"]["include_in_hospital_summary"] is False
