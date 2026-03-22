import mlflow
import mlflow.sklearn
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
from xgboost import XGBClassifier

import sys
sys.path.append(str(Path(__file__).parent))
from preprocessing import load_and_engineer

project_root = Path(__file__).parent.parent
mlflow.set_tracking_uri(f"file://{project_root}/mlruns")
mlflow.set_experiment("EMI_Classification")

def train_and_log(model, name, X_train, X_test, yc_train, yc_test):
    with mlflow.start_run(run_name=name):
        model.fit(X_train, yc_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(yc_test, y_pred)
        f1  = f1_score(yc_test, y_pred, average='weighted')
        mlflow.log_param("model", name)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_weighted", f1)
        mlflow.sklearn.log_model(model, artifact_path="model")
        print(f"\n{'='*40}")
        print(f"{name} → Accuracy: {acc:.4f} | F1: {f1:.4f}")
        print(classification_report(yc_test, y_pred,
              target_names=['Eligible','High_Risk','Not_Eligible']))
        return acc, f1, model

if __name__ == '__main__':
    X_train, X_test, yc_train, yc_test, yr_train, yr_test, feat_cols = load_and_engineer()
    
    models = [
        (LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1), "Logistic_Regression"),
        (RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1), "Random_Forest"),
        (XGBClassifier(n_estimators=100, random_state=42, eval_metric='mlogloss', n_jobs=-1), "XGBoost"),
    ]
    
    results = []
    for model, name in models:
        acc, f1, trained = train_and_log(model, name, X_train, X_test, yc_train, yc_test)
        results.append((name, acc, f1, trained))
    
    # Best model by F1
    best = max(results, key=lambda x: x[2])
    print(f"\n🏆 Best Classifier: {best[0]} — F1: {best[2]:.4f}")
    pickle.dump(best[3], open(project_root / 'models/best_classifier.pkl', 'wb'))
    print("Saved: models/best_classifier.pkl")
