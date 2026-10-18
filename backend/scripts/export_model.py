"""
Export script to train and save model artifacts exactly matching the notebook:
"Advanced Heart Disease.ipynb"
"""

import json
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import (
    AdaBoostClassifier,
    ExtraTreesClassifier,
    RandomForestClassifier,
    StackingClassifier,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def export_pipeline(data_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"Dataset loaded. Shape: {df.shape}")

    # 1. Median Imputation
    imputer = SimpleImputer(strategy="median")
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    df = df_imputed

    X_all = df.drop("target", axis=1)
    y = df["target"].astype(int)

    all_features = list(X_all.columns)
    print(f"13 features: {all_features}")

    # 2. Scaler on all features (for reference & baseline)
    scaler_all = StandardScaler()
    X_scaled = scaler_all.fit_transform(X_all)

    # 3. Random Forest Feature Importance to select top 10 features (as in Notebook Cell 8)
    rf_temp = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_temp.fit(X_scaled, y)
    importances = rf_temp.feature_importances_

    feature_df = pd.DataFrame({
        "Feature": all_features,
        "Importance": importances,
    }).sort_values(by="Importance", ascending=False)

    top_features = list(feature_df["Feature"].head(10).values)
    print(f"Top 10 selected features: {top_features}")

    # 4. Scale selected features (as in Notebook Cell 9)
    X_selected = df[top_features]
    scaler_selected = StandardScaler()
    X_selected_scaled = scaler_selected.fit_transform(X_selected)

    # 5. Split data: 70% train, 15% val, 15% test (as in Notebook Cell 10)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X_selected_scaled, y, test_size=0.3, stratify=y, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
    )

    print(f"Split sizes: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}")

    # 6. Train Hybrid Stacking Classifier (RF + SVM + KNN -> Logistic Regression)
    base_models = [
        ("rf", RandomForestClassifier(n_estimators=200, random_state=42)),
        ("svm", SVC(probability=True, random_state=42)),
        ("knn", KNeighborsClassifier(n_neighbors=7)),
    ]
    meta_model = LogisticRegression(max_iter=1000, random_state=42)

    hybrid_model = StackingClassifier(
        estimators=base_models,
        final_estimator=meta_model,
        cv=5,
    )
    print("Fitting Hybrid Stacking model...")
    hybrid_model.fit(X_train, y_train)

    # Evaluate Hybrid Model
    y_test_pred = hybrid_model.predict(X_test)
    y_test_prob = hybrid_model.predict_proba(X_test)[:, 1]
    y_train_pred = hybrid_model.predict(X_train)

    hybrid_metrics = {
        "train_accuracy": float(accuracy_score(y_train, y_train_pred)),
        "test_accuracy": float(accuracy_score(y_test, y_test_pred)),
        "precision": float(precision_score(y_test, y_test_pred)),
        "recall": float(recall_score(y_test, y_test_pred)),
        "f1_score": float(f1_score(y_test, y_test_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_test_prob)),
    }
    print("Hybrid Model Metrics:", hybrid_metrics)

    # 7. Train other individual models
    individual_models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
        "SVM": SVC(probability=True, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=7),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
        "AdaBoost": AdaBoostClassifier(n_estimators=100, random_state=42),
        "Naive Bayes": GaussianNB(),
        "Neural Network": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42),
        "Extra Trees": ExtraTreesClassifier(n_estimators=300, random_state=42),
    }

    model_metrics = {"Hybrid Stacking": hybrid_metrics}
    fitted_individual = {}

    for name, model in individual_models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
        fitted_individual[name] = model

        train_acc = float(accuracy_score(y_train, model.predict(X_train)))
        test_acc = float(accuracy_score(y_test, pred))
        prec = float(precision_score(y_test, pred, zero_division=0))
        rec = float(recall_score(y_test, pred, zero_division=0))
        f1 = float(f1_score(y_test, pred, zero_division=0))
        auc = float(roc_auc_score(y_test, prob)) if prob is not None else None

        model_metrics[name] = {
            "train_accuracy": train_acc,
            "test_accuracy": test_acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1,
            "roc_auc": auc,
            "supports_probability": prob is not None,
        }

    # 8. Save Artifacts
    joblib.dump(hybrid_model, os.path.join(output_dir, "hybrid_model.joblib"))
    joblib.dump(scaler_selected, os.path.join(output_dir, "scaler.joblib"))
    joblib.dump(scaler_all, os.path.join(output_dir, "scaler_all.joblib"))
    joblib.dump(imputer, os.path.join(output_dir, "imputer.joblib"))
    joblib.dump(fitted_individual, os.path.join(output_dir, "individual_models.joblib"))

    # Feature Importance table
    importance_list = [
        {"feature": row["Feature"], "importance": float(row["Importance"])}
        for _, row in feature_df.iterrows()
    ]

    metadata = {
        "project_name": "Advanced Heart Disease Prediction System",
        "brand_name": "HeartPredict AI",
        "version": "1.0.0",
        "target_column": "target",
        "target_classes": {
            0: {"label": "Lower Risk (Negative)", "code": "LOWER_RISK"},
            1: {"label": "Higher Risk (Positive)", "code": "HIGHER_RISK"},
        },
        "all_features": all_features,
        "selected_top_features": top_features,
        "feature_importances": importance_list,
        "hybrid_architecture": "Random Forest + SVM + KNN -> Logistic Regression Meta Learner",
        "model_metrics": model_metrics,
        "split_ratio": {"train": 0.70, "val": 0.15, "test": 0.15},
        "preprocessing_pipeline": [
            {"step": "Median Imputation", "strategy": "median"},
            {"step": "Top Feature Selection", "top_k": 10, "method": "RandomForest Feature Importance"},
            {"step": "StandardScaler", "with_mean": True, "with_std": True},
        ],
    }

    with open(os.path.join(output_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"All artifacts successfully exported to {output_dir}")
    return metadata


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    data_file = os.path.join(base_dir, "data", "heart.csv")
    artifacts_dir = os.path.join(base_dir, "artifacts")
    export_pipeline(data_file, artifacts_dir)
