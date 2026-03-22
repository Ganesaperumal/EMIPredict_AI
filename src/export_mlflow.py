import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
from pathlib import Path

# Setup local tracking
project_root = Path(__file__).parent.parent
TRACKING_URI = f"file://{project_root}/mlruns"
mlflow.set_tracking_uri(TRACKING_URI)
client = MlflowClient(tracking_uri=TRACKING_URI)

def export_metrics():
    all_runs = []
    
    # Get all experiments
    experiments = client.search_experiments()
    
    for exp in experiments:
        runs = client.search_runs(experiment_ids=[exp.experiment_id])
        for run in runs:
            run_data = {
                "experiment_name": exp.name,
                "run_id": run.info.run_id,
                "model_name": run.data.params.get("model", "Unknown"),
                "start_time": pd.to_datetime(run.info.start_time, unit='ms')
            }
            # Blend in metrics
            run_data.update(run.data.metrics)
            # Blend in params
            run_data.update(run.data.params)
            
            all_runs.append(run_data)
            
    if all_runs:
        df = pd.DataFrame(all_runs)
        output_path = project_root / 'data/mlflow_stats.parquet'
        df.to_parquet(output_path, index=False)
        print(f"✅ Successfully exported {len(all_runs)} runs to {output_path}")
        print(f"Export size: {output_path.stat().st_size / 1024:.2f} KB")
    else:
        print("❌ No runs found to export.")

if __name__ == "__main__":
    export_metrics()
