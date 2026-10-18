VALID_PATIENT_FEATURES = {
    "age": 58,
    "sex": 1,
    "cp": 2,
    "trestbps": 140.0,
    "chol": 211.0,
    "fbs": 1,
    "restecg": 0,
    "thalach": 165.0,
    "exang": 0,
    "oldpeak": 1.8,
    "slope": 2,
    "ca": 0,
    "thal": 2,
}


def test_predict_single_success(client, auth_headers_user1):
    res = client.post(
        "/api/v1/predictions/heart",
        json={"features": VALID_PATIENT_FEATURES, "model_name": "hybrid_stacking"},
        headers=auth_headers_user1,
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    pred_data = data["data"]
    assert pred_data["prediction"]["class"] in (0, 1)
    assert "label" in pred_data["prediction"]
    assert "probability" in pred_data
    assert "disclaimer" in pred_data
    assert pred_data["model"] == "Hybrid Stacking"


def test_predict_guest_success(client):
    res = client.post(
        "/api/v1/predictions/heart",
        json=VALID_PATIENT_FEATURES,
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["saved_to_history"] is False


def test_predict_missing_feature(client):
    invalid = VALID_PATIENT_FEATURES.copy()
    del invalid["chol"]
    res = client.post("/api/v1/predictions/heart", json=invalid)
    assert res.status_code == 422
    data = res.get_json()
    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_predict_out_of_range_value(client):
    invalid = VALID_PATIENT_FEATURES.copy()
    invalid["age"] = 300  # Out of range (max 120)
    res = client.post("/api/v1/predictions/heart", json=invalid)
    assert res.status_code == 422
    data = res.get_json()
    assert data["success"] is False


def test_prediction_history_isolation(client, auth_headers_user1, auth_headers_user2):
    # User 1 makes a prediction
    p_res = client.post(
        "/api/v1/predictions/heart",
        json={"features": VALID_PATIENT_FEATURES},
        headers=auth_headers_user1,
    )
    pred_id = p_res.get_json()["data"]["prediction_id"]

    # User 2 tries to view User 1's prediction
    forbidden_res = client.get(f"/api/v1/predictions/{pred_id}", headers=auth_headers_user2)
    assert forbidden_res.status_code == 403

    # User 2 tries to delete User 1's prediction
    del_res = client.delete(f"/api/v1/predictions/{pred_id}", headers=auth_headers_user2)
    assert del_res.status_code == 403

    # User 1 successfully views and deletes it
    ok_res = client.get(f"/api/v1/predictions/{pred_id}", headers=auth_headers_user1)
    assert ok_res.status_code == 200
    ok_del = client.delete(f"/api/v1/predictions/{pred_id}", headers=auth_headers_user1)
    assert ok_del.status_code == 200


def test_missing_model_artifacts_error(client):
    from app.services.model_loader import ModelManager

    mgr = ModelManager.get_instance()
    original_ready = mgr.is_ready
    original_error = mgr.load_error

    try:
        mgr.is_ready = False
        mgr.load_error = "Simulated missing artifact test"

        res = client.post("/api/v1/predictions/heart", json=VALID_PATIENT_FEATURES)
        assert res.status_code == 503
        data = res.get_json()
        assert data["success"] is False
        assert data["error"]["code"] == "MODEL_UNAVAILABLE"
    finally:
        mgr.is_ready = original_ready
        mgr.load_error = original_error

