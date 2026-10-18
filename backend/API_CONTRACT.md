# HeartPredict AI — Complete API Contract

Base URL: `http://localhost:5000/api/v1`

Uniform Response Formats:

**Success:**
```json
{
  "success": true,
  "data": {},
  "meta": {}
}
```

**Error:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable error description",
    "details": []
  }
}
```

---

## 1. Authentication APIs

### 1.1 Register
- **URL**: `/api/v1/auth/register`
- **Method**: `POST`
- **Auth**: None
- **Body**:
  ```json
  {
    "email": "doctor@hospital.org",
    "password": "SecurePassword123!",
    "full_name": "Dr. Sarah Connor"
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "success": true,
    "data": {
      "user": {
        "id": "uuid-v4",
        "email": "doctor@hospital.org",
        "full_name": "Dr. Sarah Connor",
        "has_profile": true
      },
      "access_token": "jwt-token-string",
      "refresh_token": "jwt-refresh-string"
    }
  }
  ```

### 1.2 Login
- **URL**: `/api/v1/auth/login`
- **Method**: `POST`
- **Auth**: None
- **Body**:
  ```json
  {
    "email": "doctor@hospital.org",
    "password": "SecurePassword123!"
  }
  ```
- **Response (200 OK)**:
  Returns user object, `access_token`, and `refresh_token`.

### 1.3 Logout
- **URL**: `/api/v1/auth/logout`
- **Method**: `POST`
- **Auth**: `Bearer <access_token>`
- **Response (200 OK)**:
  Revokes the token in the server blocklist.

### 1.4 Get Current User
- **URL**: `/api/v1/auth/me`
- **Method**: `GET`
- **Auth**: `Bearer <access_token>`
- **Response (200 OK)**: Returns authenticated user record.

### 1.5 Refresh Access Token
- **URL**: `/api/v1/auth/refresh`
- **Method**: `POST`
- **Auth**: `Bearer <refresh_token>`
- **Response (200 OK)**: Returns new `access_token`.

### 1.6 Change Password
- **URL**: `/api/v1/auth/change-password`
- **Method**: `POST`
- **Auth**: `Bearer <access_token>`
- **Body**:
  ```json
  {
    "old_password": "OldPassword123!",
    "new_password": "NewPassword456!"
  }
  ```

---

## 2. Patient Profile APIs

### 2.1 Get My Profile
- **URL**: `/api/v1/profiles/me`
- **Method**: `GET`
- **Auth**: `Bearer <access_token>`

### 2.2 Update Profile (Partial)
- **URL**: `/api/v1/profiles/me`
- **Method**: `PATCH`
- **Auth**: `Bearer <access_token>`
- **Body**:
  ```json
  {
    "full_name": "John Doe",
    "date_of_birth": "1985-06-20",
    "gender": "Male",
    "phone_number": "+1-555-0199",
    "blood_group": "A+",
    "height_cm": 178.0,
    "weight_kg": 76.5,
    "emergency_contact": {
      "name": "Jane Doe",
      "phone": "+1-555-0198",
      "relation": "Spouse"
    },
    "known_allergies": "Penicillin",
    "existing_medical_conditions": "Hypertension (controlled)",
    "current_medications": "Lisinopril 10mg daily",
    "family_history_heart_disease": true
  }
  ```
- **Response (200 OK)**: Returns updated profile and updated `completion_percentage`.

### 2.3 Upload Profile Photo
- **URL**: `/api/v1/profiles/me/photo`
- **Method**: `POST`
- **Auth**: `Bearer <access_token>`
- **Content-Type**: `multipart/form-data` (file key: `photo`)
- **Response (200 OK)**: Returns `photo_filename` and `photo_url`.

### 2.4 Profile Completion Details
- **URL**: `/api/v1/profiles/me/completion`
- **Method**: `GET`
- **Auth**: `Bearer <access_token>`
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "data": {
      "completion_percentage": 85,
      "is_complete": false,
      "missing_sections": ["Clinical History & Known Allergies"]
    }
  }
  ```

---

## 3. Single Heart Disease Prediction APIs

### 3.1 Run Heart Disease Prediction
- **URL**: `/api/v1/predictions/heart`
- **Method**: `POST`
- **Auth**: Optional `Bearer <access_token>` (authenticated users have results stored in history)
- **Headers**:
  - `Content-Type: application/json`
  - `Accept-Language: en` or `Accept-Language: te` (Telugu)
- **Body**:
  ```json
  {
    "features": {
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
      "thal": 2
    },
    "model_name": "hybrid_stacking",
    "save_to_history": true
  }
  ```
- **Response (200 / 201 Created)**:
  ```json
  {
    "success": true,
    "data": {
      "prediction_id": "4bf75e11-e1cb-4654-9ee7-1e53a25ef11a",
      "model": "Hybrid Stacking",
      "model_version": "1.0.0",
      "prediction": {
        "class": 1,
        "label": "Higher Risk",
        "code": "HIGHER_RISK",
        "description": "The model identified risk patterns associated with heart disease in the provided clinical features."
      },
      "probability": 0.942,
      "disclaimer": "This system is intended for research and decision-support purposes...",
      "saved_to_history": true,
      "created_at": "2026-10-18T17:15:30Z"
    }
  }
  ```

### 3.2 List Available Models
- **URL**: `/api/v1/predictions/models`
- **Method**: `GET`
- **Auth**: None

### 3.3 Prediction History
- **URL**: `/api/v1/predictions/history?page=1&per_page=10`
- **Method**: `GET`
- **Auth**: `Bearer <access_token>`

---

## 4. Bulk Prediction APIs

### 4.1 Validate File
- **URL**: `/api/v1/bulk/validate`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data` (`file`)
- **Response (200 OK)**:
  Returns row count, column detection, row-level validation errors (if any).

### 4.2 Run Bulk Prediction
- **URL**: `/api/v1/bulk/predict`
- **Method**: `POST`
- **Auth**: Optional `Bearer <access_token>`
- **Content-Type**: `multipart/form-data` (`file`)
- **Response (201 Created)**:
  ```json
  {
    "success": true,
    "data": {
      "job_id": "uuid-v4",
      "filename": "patients.xlsx",
      "status": "completed",
      "total_records": 150,
      "positive_records": 82,
      "negative_records": 68,
      "results_sample": [ ... ],
      "download_url": "/api/v1/bulk/jobs/uuid-v4/download"
    }
  }
  ```

### 4.3 Download Results Spreadsheet
- **URL**: `/api/v1/bulk/jobs/<job_id>/download`
- **Method**: `GET`
- **Auth**: Optional

### 4.4 Download Blank Excel Template
- **URL**: `/api/v1/bulk/template`
- **Method**: `GET`
- **Auth**: None

---

## 5. Lifestyle Risk Assessment APIs

### 5.1 Submit Lifestyle Questionnaire
- **URL**: `/api/v1/lifestyle-assessments`
- **Method**: `POST`
- **Auth**: Optional `Bearer <access_token>`
- **Body**:
  ```json
  {
    "activity": 3,
    "diet": 3,
    "smoking": 4,
    "alcohol": 4,
    "sleep": 3,
    "stress": 2,
    "weight": 3
  }
  ```
  *(1 = Highest risk behavior, 4 = Optimal/protective habit)*
- **Response (201 Created)**:
  ```json
  {
    "success": true,
    "data": {
      "assessment_id": "uuid",
      "score": 24.5,
      "category": "lower",
      "category_label": "Lower Risk",
      "category_code": "LOWER_RISK",
      "breakdown": [
        { "key": "smoking", "label": "Smoking & Tobacco", "score": 0.0, "weight": 0.22 },
        { "key": "activity", "label": "Physical Activity", "score": 30.0, "weight": 0.18 }
      ],
      "recommendations": [ ... ],
      "scoring_explanation": "The lifestyle risk score (24.5/100) is a weighted calculation...",
      "disclaimer": "This is an educational lifestyle assessment..."
    }
  }
  ```

---

## 6. Assessment History & Hospital Summary APIs

### 6.1 Combined History Timeline
- **URL**: `/api/v1/assessments/history?type=all&page=1&per_page=10`
- **Method**: `GET`
- **Auth**: `Bearer <access_token>`

### 6.2 Toggle Hospital Summary Inclusion
- **URL**: `/api/v1/assessments/<assessment_id>/hospital-summary`
- **Method**: `PATCH`
- **Auth**: `Bearer <access_token>`
- **Body**: `{"include_in_hospital_summary": true}`

### 6.3 Hospital Summary Preview (HTML)
- **URL**: `/api/v1/hospital-summary/preview`
- **Method**: `GET`
- **Auth**: `Bearer <access_token>`
- **Response**: Formatted HTML page suitable for browser printing or saving as PDF.

### 6.4 Hospital Summary Share (Explicit Consent)
- **URL**: `/api/v1/hospital-summary/share`
- **Method**: `POST`
- **Auth**: `Bearer <access_token>`
- **Body**:
  ```json
  {
    "consent": true,
    "purpose": "Consultation with cardiologist Dr. Miller",
    "recipient_email": "dr.miller@cardiology.org"
  }
  ```

---

## 7. Project Metadata & Health APIs

- `GET /api/v1/health`: Server status, database connectivity, and ML models readiness.
- `GET /api/v1/models`: List of all 13 evaluated models and their architecture.
- `GET /api/v1/project/info`: Project overview, preprocessing pipeline, and research background.
- `GET /api/v1/project/features`: Definitions, valid ranges, units, and descriptions for all 13 features.
- `GET /api/v1/project/feature-importance`: Real verified feature importances from the notebook.
- `GET /api/v1/project/metrics`: Real verified evaluation metrics from the notebook.
