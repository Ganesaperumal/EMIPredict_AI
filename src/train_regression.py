import mlflow
import mlflow.sklearn
import pickle
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

import sys
sys.path.append(str(Path(__file__).parent))
from preprocessing import load_and_engineer

project_root = Path(__file__).parent.parent
mlflow.set_tracking_uri(f"file://{project_root}/mlruns")
mlflow.set_experiment("EMI_Regression")

def train_and_log(model, name, X_train, X_test, yr_train, yr_test):
    with mlflow.start_run(run_name=name):
        model.fit(X_train, yr_train)
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(yr_test, y_pred))
        r2   = r2_score(yr_test, y_pred)
        mlflow.log_param("model", name)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.sklearn.log_model(model, artifact_path="model")
        print(f"\n{'='*40}")
        print(f"{name} → RMSE: {rmse:.2f} | R²: {r2:.4f}")
        return rmse, r2, model

if __name__ == '__main__':
    X_train, X_test, yc_train, yc_test, yr_train, yr_test, feat_cols = load_and_engineer()
    
    models = [
        (LinearRegression(), "Linear_Regression"),
        (RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1), "Random_Forest"),
        (XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1), "XGBoost"),
    ]
    
    results = []
    for model, name in models:
        rmse, r2, trained = train_and_log(model, name, X_train, X_test, yr_train, yr_test)
        results.append((name, rmse, r2, trained))
    
    # Best model by lowest RMSE
    best = min(results, key=lambda x: x[1])
    print(f"\n🏆 Best Regressor: {best[0]} — RMSE: {best[1]:.2f}")
    pickle.dump(best[3], open(project_root / 'models/best_regressor.pkl', 'wb'))
    print("Saved: models/best_regressor.pkl")
