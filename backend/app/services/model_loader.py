import json
import logging
import os
import joblib
import numpy as np
import pandas as pd
from app.utils.errors import BadRequestError, ModelUnavailableError

logger = logging.getLogger("heartpredict.model_loader")


class ModelManager:
    _instance = None

    def __init__(self, artifacts_dir: str = None):
        self.artifacts_dir = artifacts_dir
        self.hybrid_model = None
        self.scaler = None
        self.scaler_all = None
        self.imputer = None
        self.individual_models = {}
        self.metadata = {}
        self.is_ready = False
        self.load_error = None

    @classmethod
    def get_instance(cls, artifacts_dir: str = None):
        if cls._instance is None:
            cls._instance = cls(artifacts_dir)
        return cls._instance

    def initialize(self, artifacts_dir: str):
        self.artifacts_dir = artifacts_dir
        self.is_ready = False
        self.load_error = None

        if not os.path.exists(artifacts_dir):
            self.load_error = f"Artifacts directory '{artifacts_dir}' does not exist. Please run export_model.py."
            logger.warning(self.load_error)
            return

        hybrid_path = os.path.join(artifacts_dir, "hybrid_model.joblib")
        scaler_path = os.path.join(artifacts_dir, "scaler.joblib")
        scaler_all_path = os.path.join(artifacts_dir, "scaler_all.joblib")
        imputer_path = os.path.join(artifacts_dir, "imputer.joblib")
        individual_path = os.path.join(artifacts_dir, "individual_models.joblib")
        meta_path = os.path.join(artifacts_dir, "metadata.json")

        missing = []
        for name, p in [
            ("hybrid_model", hybrid_path),
            ("scaler", scaler_path),
            ("imputer", imputer_path),
            ("metadata", meta_path),
        ]:
            if not os.path.exists(p):
                missing.append(name)

        if missing:
            self.load_error = (
                f"Missing required model artifacts: {', '.join(missing)}. "
                f"Run 'python backend/scripts/export_model.py' to generate them."
            )
            logger.warning(self.load_error)
            return

        try:
            self.hybrid_model = joblib.load(hybrid_path)
            self.scaler = joblib.load(scaler_path)
            self.imputer = joblib.load(imputer_path)

            if os.path.exists(scaler_all_path):
                self.scaler_all = joblib.load(scaler_all_path)

            if os.path.exists(individual_path):
                self.individual_models = joblib.load(individual_path)

            with open(meta_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

            self.is_ready = True
            logger.info("HeartPredict AI model artifacts successfully loaded and validated.")
        except Exception as e:
            self.load_error = f"Failed to load model artifacts: {str(e)}"
            logger.error(self.load_error, exc_info=True)
            self.is_ready = False

    def check_ready(self):
        if not self.is_ready:
            raise ModelUnavailableError(
                self.load_error
                or "Machine learning model artifacts are currently unavailable on this server."
            )

    def get_selected_features(self) -> list[str]:
        return self.metadata.get(
            "selected_top_features",
            ["cp", "thalach", "ca", "oldpeak", "thal", "age", "chol", "trestbps", "exang", "slope"],
        )

    def get_all_features(self) -> list[str]:
        return self.metadata.get(
            "all_features",
            ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"],
        )

    def predict(self, feature_dict: dict, model_name: str = "hybrid_stacking") -> dict:
        self.check_ready()

        # Select model
        selected_model = None
        model_display_name = "Hybrid Stacking"
        if model_name in (None, "", "hybrid_stacking", "Hybrid Stacking", "hybrid"):
            selected_model = self.hybrid_model
            model_display_name = "Hybrid Stacking"
        else:
            # Check individual models
            found = False
            for k, m in self.individual_models.items():
                if k.lower() == model_name.lower() or k.lower().replace(" ", "_") == model_name.lower():
                    selected_model = m
                    model_display_name = k
                    found = True
                    break
            if not found:
                available = ["hybrid_stacking"] + list(self.individual_models.keys())
                raise BadRequestError(
                    f"Selected model '{model_name}' is not available. Available models: {available}"
                )

        # Build feature vector matching selected top features
        top_features = self.get_selected_features()
        missing_top = [f for f in top_features if f not in feature_dict]
        if missing_top:
            raise BadRequestError(f"Missing required clinical features: {missing_top}")

        # Extract values in top_features order
        raw_values = [feature_dict[col] for col in top_features]
        df_row = pd.DataFrame([raw_values], columns=top_features)

        # Scale using the fitted scaler
        X_scaled = self.scaler.transform(df_row)

        # Run prediction
        raw_pred = int(selected_model.predict(X_scaled)[0])

        # Probability
        prob = None
        if hasattr(selected_model, "predict_proba"):
            try:
                probs = selected_model.predict_proba(X_scaled)[0]
                prob = float(probs[1]) if len(probs) > 1 else float(probs[0])
            except Exception:
                prob = None

        return {
            "prediction_class": raw_pred,
            "prediction_label": "Higher Risk" if raw_pred == 1 else "Lower Risk",
            "prediction_code": "HIGHER_RISK" if raw_pred == 1 else "LOWER_RISK",
            "probability": prob,
            "model_name": model_display_name,
            "model_version": self.metadata.get("version", "1.0.0"),
        }

    def predict_batch(self, df_rows: pd.DataFrame, model_name: str = "hybrid_stacking") -> list[dict]:
        self.check_ready()

        top_features = self.get_selected_features()
        missing_top = [f for f in top_features if f not in df_rows.columns]
        if missing_top:
            raise BadRequestError(f"Uploaded data is missing features required by the model: {missing_top}")

        X_selected = df_rows[top_features]
        X_scaled = self.scaler.transform(X_selected)

        selected_model = self.hybrid_model
        if model_name and model_name.lower() not in ("hybrid_stacking", "hybrid", "default"):
            for k, m in self.individual_models.items():
                if k.lower() == model_name.lower():
                    selected_model = m
                    break

        preds = selected_model.predict(X_scaled)
        probs = None
        if hasattr(selected_model, "predict_proba"):
            try:
                probs = selected_model.predict_proba(X_scaled)[:, 1]
            except Exception:
                probs = None

        results = []
        for i in range(len(preds)):
            raw_p = int(preds[i])
            results.append({
                "row_index": i + 1,
                "prediction_class": raw_p,
                "prediction_label": "Higher Risk" if raw_p == 1 else "Lower Risk",
                "probability": float(probs[i]) if probs is not None else None,
            })
        return results

    def get_models_info(self) -> list[dict]:
        models_list = []
        if self.hybrid_model is not None:
            models_list.append({
                "id": "hybrid_stacking",
                "name": "Hybrid Stacking Classifier",
                "type": "Ensemble (RF + SVM + KNN -> Logistic Regression)",
                "is_default": True,
                "supports_probability": True,
                "status": "active" if self.is_ready else "unavailable",
            })

        for name, model in self.individual_models.items():
            models_list.append({
                "id": name.lower().replace(" ", "_"),
                "name": name,
                "type": type(model).__name__,
                "is_default": False,
                "supports_probability": hasattr(model, "predict_proba"),
                "status": "active" if self.is_ready else "unavailable",
            })
        return models_list
