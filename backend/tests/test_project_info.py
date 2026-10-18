def test_project_info_endpoints(client):
    # Health check
    h_res = client.get("/api/v1/health")
    assert h_res.status_code == 200
    h_data = h_res.get_json()["data"]
    assert h_data["database_connected"] is True
    assert h_data["models_ready"] is True

    # Models list
    m_res = client.get("/api/v1/models")
    assert m_res.status_code == 200
    m_data = m_res.get_json()["data"]
    assert len(m_data["models"]) > 0

    # Project info
    p_res = client.get("/api/v1/project/info")
    assert p_res.status_code == 200
    p_data = p_res.get_json()["data"]
    assert p_data["name"] == "Advanced Heart Disease Prediction System"

    # Features
    f_res = client.get("/api/v1/project/features")
    assert f_res.status_code == 200
    f_data = f_res.get_json()["data"]
    assert len(f_data["features"]) == 13

    # Feature Importance
    fi_res = client.get("/api/v1/project/feature-importance")
    assert fi_res.status_code == 200
    fi_data = fi_res.get_json()["data"]
    assert len(fi_data["feature_importances"]) > 0

    # Real Metrics
    met_res = client.get("/api/v1/project/metrics")
    assert met_res.status_code == 200
    met_data = met_res.get_json()["data"]
    assert "metrics" in met_data
    assert "Hybrid Stacking" in met_data["metrics"]


def test_cors_headers(client):
    res = client.get("/api/v1/health", headers={"Origin": "http://localhost:5173"})
    assert res.status_code == 200
    assert res.headers.get("Access-Control-Allow-Origin") == "http://localhost:5173"

