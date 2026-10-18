def test_hospital_summary_endpoints(client, auth_headers_user1):
    # Get JSON summary data
    sum_res = client.get("/api/v1/hospital-summary", headers=auth_headers_user1)
    assert sum_res.status_code == 200
    sum_data = sum_res.get_json()["data"]
    assert "patient_name" in sum_data
    assert "heart_predictions" in sum_data
    assert "disclaimer" in sum_data

    # Preview HTML
    prev_res = client.get("/api/v1/hospital-summary/preview", headers=auth_headers_user1)
    assert prev_res.status_code == 200
    assert "text/html" in prev_res.headers.get("Content-Type", "")
    assert b"HeartPredict AI" in prev_res.data

    # Share with explicit consent
    share_res = client.post(
        "/api/v1/hospital-summary/share",
        json={"consent": True, "purpose": "Cardiologist Review"},
        headers=auth_headers_user1,
    )
    assert share_res.status_code == 200
    assert share_res.get_json()["data"]["status"] == "prepared"

    # Share without consent fails
    no_consent_res = client.post(
        "/api/v1/hospital-summary/share",
        json={"consent": False},
        headers=auth_headers_user1,
    )
    assert no_consent_res.status_code == 422
