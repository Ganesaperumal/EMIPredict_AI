import mlflow
from mlflow.tracking import MlflowClient
from pathlib import Path

# Setup local tracking
project_root = Path(__file__).parent.parent
TRACKING_URI = f"file://{project_root}/mlruns"
mlflow.set_tracking_uri(TRACKING_URI)
client = MlflowClient(tracking_uri=TRACKING_URI)

def register_best(experiment_name, metric, higher_is_better, registry_name):
    exp = client.get_experiment_by_name(experiment_name)
    runs = client.search_runs(
        experiment_ids=[exp.experiment_id],
        order_by=[f"metrics.{metric} {'DESC' if higher_is_better else 'ASC'}"],
        max_results=1
    )
    if not runs:
        print(f"No runs found for {experiment_name}")
        return
    
    best_run = runs[0]
    run_id = best_run.info.run_id
    metric_val = best_run.data.metrics[metric]
    model_name = best_run.data.params.get("model", "Unknown")
    
    print(f"\n{experiment_name}")
    print(f"  Best run: {model_name} | {metric}: {metric_val:.4f}")
    print(f"  Run ID: {run_id}")
    
    model_uri = f"runs:/{run_id}/model"
    mv = mlflow.register_model(model_uri=model_uri, name=registry_name)
    print(f"  Registered as: {registry_name} v{mv.version}")
    
    client.set_registered_model_tag(registry_name, "best_model", model_name)
    client.set_registered_model_tag(registry_name, metric, str(round(metric_val, 4)))

if __name__ == '__main__':
    register_best("EMI_Classification", "f1_weighted", True,  "EMI_Classifier")
    register_best("EMI_Regression",     "rmse",        False, "EMI_Regressor")
    print("\n✅ Both models registered in MLflow Model Registry!")
