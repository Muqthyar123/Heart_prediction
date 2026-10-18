import io
import pandas as pd
from app.utils.validation import REQUIRED_CLINICAL_FEATURES


def test_download_template(client):
    res = client.get("/api/v1/bulk/template")
    assert res.status_code == 200
    assert "spreadsheet" in res.headers.get("Content-Type", "")


def test_validate_and_predict_bulk_csv(client, auth_headers_user1):
    data = [
        [58, 1, 2, 140.0, 211.0, 1, 0, 165.0, 0, 1.8, 2, 0, 2],
        [67, 1, 0, 160.0, 286.0, 0, 2, 108.0, 1, 1.5, 1, 3, 1],
    ]
    df = pd.DataFrame(data, columns=REQUIRED_CLINICAL_FEATURES)

    # First request: validate
    csv_bytes_1 = io.BytesIO()
    df.to_csv(csv_bytes_1, index=False)
    csv_bytes_1.seek(0)

    val_res = client.post(
        "/api/v1/bulk/validate",
        data={"file": (csv_bytes_1, "patients.csv")},
        content_type="multipart/form-data",
    )
    assert val_res.status_code == 200
    val_data = val_res.get_json()["data"]
    assert val_data["is_valid"] is True
    assert val_data["total_rows"] == 2

    # Second request: predict with fresh stream
    csv_bytes_2 = io.BytesIO()
    df.to_csv(csv_bytes_2, index=False)
    csv_bytes_2.seek(0)

    pred_res = client.post(
        "/api/v1/bulk/predict",
        data={"file": (csv_bytes_2, "patients.csv")},
        content_type="multipart/form-data",
        headers=auth_headers_user1,
    )
    assert pred_res.status_code == 201
    pred_data = pred_res.get_json()["data"]
    assert pred_data["total_records"] == 2
    assert "download_url" in pred_data


def test_bulk_missing_columns(client):
    df = pd.DataFrame([[50, 1]], columns=["age", "sex"])
    csv_bytes = io.BytesIO()
    df.to_csv(csv_bytes, index=False)
    csv_bytes.seek(0)

    val_res = client.post(
        "/api/v1/bulk/validate",
        data={"file": (csv_bytes, "incomplete.csv")},
        content_type="multipart/form-data",
    )
    assert val_res.status_code == 422
    data = val_res.get_json()
    assert data["success"] is False
