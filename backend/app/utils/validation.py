import math
import re
from datetime import datetime
from app.utils.errors import ValidationError

CLINICAL_FEATURE_DEFS = {
    "age": {
        "name": "Age",
        "type": "integer",
        "min": 1,
        "max": 120,
        "unit": "years",
        "description": "Patient age in years.",
    },
    "sex": {
        "name": "Sex / Gender",
        "type": "categorical",
        "allowed_values": [0, 1],
        "options": {0: "Female", 1: "Male"},
        "description": "Biological sex (0 = Female, 1 = Male).",
    },
    "cp": {
        "name": "Chest Pain Type",
        "type": "categorical",
        "allowed_values": [0, 1, 2, 3],
        "options": {
            0: "Typical Angina",
            1: "Atypical Angina",
            2: "Non-anginal Pain",
            3: "Asymptomatic",
        },
        "description": "Type of chest pain reported by patient.",
    },
    "trestbps": {
        "name": "Resting Blood Pressure",
        "type": "float",
        "min": 50.0,
        "max": 260.0,
        "unit": "mm Hg",
        "description": "Resting systolic blood pressure upon admission.",
    },
    "chol": {
        "name": "Serum Cholesterol",
        "type": "float",
        "min": 80.0,
        "max": 650.0,
        "unit": "mg/dl",
        "description": "Serum cholesterol level.",
    },
    "fbs": {
        "name": "Fasting Blood Sugar > 120 mg/dl",
        "type": "categorical",
        "allowed_values": [0, 1],
        "options": {0: "False (<= 120 mg/dl)", 1: "True (> 120 mg/dl)"},
        "description": "Fasting blood sugar indicator (1 if > 120 mg/dl, 0 otherwise).",
    },
    "restecg": {
        "name": "Resting ECG Results",
        "type": "categorical",
        "allowed_values": [0, 1, 2],
        "options": {
            0: "Normal",
            1: "ST-T Wave Abnormality",
            2: "Left Ventricular Hypertrophy",
        },
        "description": "Resting electrocardiographic results.",
    },
    "thalach": {
        "name": "Maximum Heart Rate Achieved",
        "type": "float",
        "min": 50.0,
        "max": 250.0,
        "unit": "bpm",
        "description": "Peak heart rate during exercise tolerance test.",
    },
    "exang": {
        "name": "Exercise-Induced Angina",
        "type": "categorical",
        "allowed_values": [0, 1],
        "options": {0: "No", 1: "Yes"},
        "description": "Presence of angina during physical exertion.",
    },
    "oldpeak": {
        "name": "ST Depression",
        "type": "float",
        "min": 0.0,
        "max": 10.0,
        "unit": "mm",
        "description": "ST depression induced by exercise relative to rest.",
    },
    "slope": {
        "name": "Slope of the Peak Exercise ST Segment",
        "type": "categorical",
        "allowed_values": [0, 1, 2],
        "options": {0: "Upsloping", 1: "Flat", 2: "Downsloping"},
        "description": "Slope direction of the peak ST segment.",
    },
    "ca": {
        "name": "Major Vessels Colored by Fluoroscopy",
        "type": "categorical",
        "allowed_values": [0, 1, 2, 3, 4],
        "options": {0: "0", 1: "1", 2: "2", 3: "3", 4: "4"},
        "description": "Number of major blood vessels (0-4) visualized by fluoroscopy.",
    },
    "thal": {
        "name": "Thalassemia",
        "type": "categorical",
        "allowed_values": [0, 1, 2, 3],
        "options": {
            0: "Normal / Unspecified",
            1: "Fixed Defect",
            2: "Normal Blood Flow",
            3: "Reversible Defect",
        },
        "description": "Thalassemia blood disorder category (0-3).",
    },
}

REQUIRED_CLINICAL_FEATURES = list(CLINICAL_FEATURE_DEFS.keys())


def validate_clinical_inputs(data: dict) -> tuple[dict, list[str]]:
    """
    Validates a dictionary containing the 13 clinical features.
    Returns (cleaned_dict, error_list).
    """
    cleaned = {}
    errors = []

    for feature_name, definition in CLINICAL_FEATURE_DEFS.items():
        if feature_name not in data or data[feature_name] is None:
            errors.append(f"Missing required clinical feature: '{feature_name}'.")
            continue

        raw_val = data[feature_name]

        # Convert to float or int
        try:
            val = float(raw_val)
        except (ValueError, TypeError):
            errors.append(f"Feature '{feature_name}' must be numeric, got: {raw_val}.")
            continue

        if math.isnan(val) or math.isinf(val):
            errors.append(f"Feature '{feature_name}' must be a finite number.")
            continue

        # Check bounds / allowed values
        if "allowed_values" in definition:
            int_val = int(round(val))
            if int_val not in definition["allowed_values"]:
                errors.append(
                    f"Feature '{feature_name}' value {val} is invalid. Allowed: {definition['allowed_values']}."
                )
            else:
                cleaned[feature_name] = int_val
        else:
            min_val = definition.get("min")
            max_val = definition.get("max")
            if min_val is not None and val < min_val:
                errors.append(f"Feature '{feature_name}' value {val} is below minimum ({min_val}).")
            elif max_val is not None and val > max_val:
                errors.append(f"Feature '{feature_name}' value {val} exceeds maximum ({max_val}).")
            else:
                cleaned[feature_name] = int(val) if definition.get("type") == "integer" else float(val)

    return cleaned, errors


def validate_email_address(email: str) -> bool:
    if not email or len(email) > 254:
        return False
    pattern = r"^[\w\.\+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$"
    return bool(re.match(pattern, email))


def parse_date_safe(date_str: str) -> datetime | None:
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None
