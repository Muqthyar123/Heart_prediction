def test_get_and_update_profile(client, auth_headers_user1):
    # Initial profile check
    res = client.get("/api/v1/profiles/me", headers=auth_headers_user1)
    assert res.status_code == 200
    data = res.get_json()["data"]["profile"]
    assert data["full_name"] == "Alice Smith"

    # Update profile
    update_payload = {
        "date_of_birth": "1990-05-15",
        "gender": "Female",
        "phone_number": "+1234567890",
        "blood_group": "O+",
        "height_cm": 165.0,
        "weight_kg": 60.0,
        "emergency_contact": {
            "name": "Jane Smith",
            "phone": "+1987654321",
            "relation": "Mother",
        },
    }
    patch_res = client.patch("/api/v1/profiles/me", json=update_payload, headers=auth_headers_user1)
    assert patch_res.status_code == 200
    p_data = patch_res.get_json()["data"]["profile"]
    assert p_data["blood_group"] == "O+"
    assert p_data["completion_percentage"] > 50

    # Completion breakdown check
    comp_res = client.get("/api/v1/profiles/me/completion", headers=auth_headers_user1)
    assert comp_res.status_code == 200
    comp_data = comp_res.get_json()["data"]
    assert "completion_percentage" in comp_data


def test_user_profile_isolation(client, auth_headers_user1, auth_headers_user2):
    # User 1 sets phone number
    client.patch("/api/v1/profiles/me", json={"phone_number": "111-222-3333"}, headers=auth_headers_user1)

    # User 2 checks profile
    u2_res = client.get("/api/v1/profiles/me", headers=auth_headers_user2)
    assert u2_res.status_code == 200
    u2_data = u2_res.get_json()["data"]["profile"]
    assert u2_data["phone_number"] != "111-222-3333"
