# HeartPredict AI — Flask Backend

This repository houses the Python Flask backend for **“Advanced Heart Disease Prediction System,”** branded as **HeartPredict AI**. It provides the complete set of RESTful APIs consumed by the React + TypeScript frontend, serving machine-learning predictions, batch file processing, patient profiles, lifestyle evaluations, assessment histories, and clinical summaries.

---

## 1. Machine Learning Integration

The backend directly incorporates the machine-learning pipeline and model architecture researched and verified in the project's original Jupyter notebook (`Advanced Heart Disease.ipynb`):

- **Dataset**: Cleveland/Hungarian/Switzerland/Long Beach 1025-row cardiovascular dataset (`heart.csv`).
- **13 Clinical Biomarkers**: `age`, `sex`, `cp`, `trestbps`, `chol`, `fbs`, `restecg`, `thalach`, `exang`, `oldpeak`, `slope`, `ca`, `thal`.
- **Hybrid Stacking Classifier**:
  $$\text{Random Forest} + \text{SVM} + \text{KNN} \longrightarrow \text{Logistic Regression (Meta Learner)} \longrightarrow \text{Final Output}$$
- **Data Preprocessing**:
  1. Median Imputation (`SimpleImputer(strategy='median')`)
  2. Top 10 Feature Selection via Random Forest feature importances: `['cp', 'thalach', 'ca', 'oldpeak', 'thal', 'age', 'chol', 'trestbps', 'exang', 'slope']`
  3. Feature Normalization (`StandardScaler`)
- **Preserved Artifacts**:
  - `artifacts/hybrid_model.joblib`: Trained StackingClassifier
  - `artifacts/scaler.joblib`: Fitted StandardScaler
  - `artifacts/imputer.joblib`: Fitted SimpleImputer
  - `artifacts/individual_models.joblib`: 9 individual models (Logistic Regression, Random Forest, SVM, KNN, Decision Tree, Naive Bayes, AdaBoost, MLP, Extra Trees)
  - `artifacts/metadata.json`: Feature importance weights, real training/testing accuracy scores, and schema definitions

---

## 2. Project Directory Structure

```text
backend/
├── app/
│   ├── __init__.py           # Flask Application Factory (create_app)
│   ├── config.py             # Environment configurations (Dev, Test, Prod)
│   ├── extensions.py         # SQLAlchemy, Migrate, JWTManager, CORS
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── bulk.py           # BulkJob and BulkPredictionResult
│   │   ├── hospital_summary.py# HospitalSummaryPreference and ConsentRecord
│   │   ├── lifestyle.py      # LifestyleAssessment
│   │   ├── prediction.py     # HeartPrediction
│   │   ├── profile.py        # PatientProfile
│   │   ├── token.py          # TokenBlocklist (JWT revocation)
│   │   └── user.py           # User account
│   ├── routes/               # API route Blueprints
│   │   ├── assessments.py    # Combined assessment timeline
│   │   ├── auth.py           # Registration, login, logout, password change
│   │   ├── bulk.py           # Batch file validation and predictions
│   │   ├── dashboard.py      # Patient dashboard summary & recent activity
│   │   ├── hospital_summary.py# Printable clinical summary & consent sharing
│   │   ├── lifestyle.py      # Lifestyle questionnaire & scoring
│   │   ├── predictions.py    # Single patient prediction endpoints
│   │   ├── profiles.py       # Patient profile management & photos
│   │   └── project_info.py   # Health, model list, metrics, feature info
│   ├── schemas/              # Marshmallow input/output schemas
│   ├── services/             # Core business logic & ML loader
│   │   ├── assessment_service.py
│   │   ├── auth_service.py
│   │   ├── bulk_prediction_service.py
│   │   ├── hospital_summary_service.py
│   │   ├── lifestyle_service.py
│   │   ├── model_loader.py   # Singleton artifact loader & predictor
│   │   ├── prediction_service.py
│   │   └── profile_service.py
│   └── utils/                # Helper utilities
│       ├── errors.py         # Error hierarchy & standardized format
│       ├── file_handling.py  # Secure uploads & path traversal prevention
│       ├── i18n.py           # English and Telugu localization
│       ├── security.py       # Password hashing & JWT blocklist
│       └── validation.py     # 13 clinical biomarker range validators
├── artifacts/                # Exported model joblib files & metadata
├── data/                     # heart.csv reference dataset
├── migrations/               # Alembic database migrations
├── scripts/
│   └── export_model.py       # Reproducible notebook pipeline exporter
├── tests/                    # Automated pytest test suite (23 tests)
├── uploads/                  # Secure upload directory (profiles, bulk files)
├── .env.example              # Environment variables template
├── .gitignore
├── requirements.txt          # Python dependencies
└── run.py                    # Application entry point
```

---

## 3. Quickstart & Installation

### Prerequisites
- Python 3.11+
- Virtual environment tool (`venv` or `conda`)

### Step 1: Install Dependencies
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Key variables:
- `SECRET_KEY`: Secret string for Flask session signing.
- `JWT_SECRET_KEY`: Secret string for JWT tokens.
- `DATABASE_URL`: Defaults to `sqlite:///heartpredict.db` for local development.
- `CORS_ORIGINS`: Comma-delimited list of allowed frontends (`http://localhost:3000,http://localhost:5173`).

### Step 3: Run Database Migrations
```bash
flask db upgrade
```
*(If setting up a fresh database, `flask db init && flask db migrate -m "Initial schema" && flask db upgrade`)*

### Step 4: Export Machine Learning Artifacts
To regenerate or inspect model artifacts from the reference dataset:
```bash
python scripts/export_model.py
```
This script trains the Hybrid Stacking Classifier and exports `hybrid_model.joblib`, `scaler.joblib`, `imputer.joblib`, `individual_models.joblib`, and `metadata.json` into `backend/artifacts/`.

### Step 5: Start the Backend Server
```bash
python run.py
```
The server will start at: `http://127.0.0.1:5000`

---

## 4. Running Automated Tests

Run the complete test suite with pytest:
```bash
python -m pytest tests -v
```
All 23 automated tests cover:
- User registration, duplicate detection, weak password rejection, and login.
- JWT blocklist and token revocation on logout.
- Patient profile creation, partial patch, deletion, and completion percentage calculation.
- Object-level security (ensuring User 1 cannot view or modify User 2's profile or predictions).
- Single prediction input range validation, guest access, and authenticated history saving.
- Missing model artifact handling (returning 503 `MODEL_UNAVAILABLE`).
- Batch Excel/CSV file validation, column presence checks, and row predictions.
- Transparent lifestyle questionnaire scoring across 7 lifestyle domains.
- Assessment timeline filtering and hospital summary toggle.
- Clinical hospital summary preview and explicit consent sharing.
- Feature definitions, notebook verified evaluation metrics, and CORS headers.

---

## 5. Connecting the React Frontend

The React frontend in `frontend_heart/` is pre-configured to communicate with this backend:

1. In `frontend_heart/.env` (or `.env.local`):
   ```env
   VITE_API_URL=http://localhost:5000/api/v1
   ```
2. When the backend is online, requests to `/predictions/heart`, `/bulk/predict`, and `/lifestyle-assessments` automatically call the live Flask ML pipeline.
3. If the backend is stopped or unavailable, the frontend gracefully falls back to local simulation without crashing.

---

## 6. PostgreSQL Production Setup

To transition from local SQLite to PostgreSQL:

1. Install psycopg2:
   ```bash
   pip install psycopg2-binary
   ```
2. Set your production database URL in `.env`:
   ```env
   DATABASE_URL=postgresql://db_user:secure_password@localhost:5432/heartpredict_production
   ```
3. Run migrations on the new database:
   ```bash
   flask db upgrade
   ```

---

## 7. Medical Safety & Disclaimer

> [!IMPORTANT]
> This application is intended strictly for research and clinical decision support. Predictions produced by the machine learning models must not be used as a standalone medical diagnosis. All clinical findings must be verified by licensed healthcare practitioners.
