import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from mlflow.tracking import MlflowClient
import sys
sys.path.append(str(Path(__file__).parent.parent / 'src'))
from styles import apply_glass_theme
from navigation import render_sidebar_nav

st.set_page_config(page_title="Model Performance", page_icon="🎡", layout="wide")
apply_glass_theme()

# Custom Navigation
render_sidebar_nav("pages/Model_Metrics.py")


st.markdown("""
<div class="glass-header" style="--header-bg: linear-gradient(135deg, rgba(255, 241, 242, 0.7), rgba(254, 205, 211, 0.7)); --header-border: rgba(255, 255, 255, 0.5);">
    <h1>🏆 Model Performance Dashboard</h1>
    <p>Comparison of all trained models via MLflow experiment tracking</p>
</div>
""", unsafe_allow_html=True)





PROJECT_ROOT = Path(__file__).parent.parent
TRACKING_URI = f"file://{PROJECT_ROOT}/mlruns"

@st.cache_data
def get_runs(experiment_name):
    static_stats_path = PROJECT_ROOT / 'data/mlflow_stats.parquet'
    
    # Try loading from static export first (useful for Cloud deployment)
    if static_stats_path.exists():
        df_static = pd.read_parquet(static_stats_path)
        df_filtered = df_static[df_static['experiment_name'] == experiment_name]
        if not df_filtered.empty:
            # Format to match the original output (Run column + metrics)
            df_filtered = df_filtered.rename(columns={'model_name': 'Run'})
            # Drop MLflow specific columns that aren't metrics
            cols_to_drop = ['experiment_name', 'run_id', 'start_time', 'model']
            return df_filtered.drop(columns=[c for c in cols_to_drop if c in df_filtered.columns])

    # Fallback to local MLflow (if mlruns directory exists)
    if not (PROJECT_ROOT / "mlruns").exists():
        return pd.DataFrame()
        
    try:
        client = MlflowClient(tracking_uri=TRACKING_URI)
        exp = client.get_experiment_by_name(experiment_name)
        if not exp:
            return pd.DataFrame()
        runs = client.search_runs(experiment_ids=[exp.experiment_id])
        rows = []
        for r in runs:
            row = {'Run': r.data.params.get('model', r.info.run_id[:8])}
            row.update(r.data.metrics)
            rows.append(row)
        return pd.DataFrame(rows)
    except Exception:
        return pd.DataFrame()

# ── Styling Helpers ──────────────────────────────────────────────────
def highlight_clf(s):
    is_max = s == s.max()
    return ['color: #10b981; font-weight: bold;' if v else '' for v in is_max.tolist()]

def highlight_reg_min(s):
    is_min = s == s.min()
    return ['color: #3b82f6; font-weight: bold;' if v else '' for v in is_min.tolist()]

def highlight_reg_max(s):
    is_max = s == s.max()
    return ['color: #3b82f6; font-weight: bold;' if v else '' for v in is_max.tolist()]

# ── Classification ────────────────────────────────────────────────────
st.subheader("🟢 Classification Models — EMI Eligibility")
clf_df = get_runs("EMI_Classification")

if not clf_df.empty:
    clf_df = clf_df.sort_values('f1_weighted', ascending=False).reset_index(drop=True)
    clf_df = clf_df.dropna(axis=1, how='all') # Drop 'None' columns (like regression metrics)
    
    # Apply Green Bold to Highest Values
    styled_clf = clf_df.style.apply(highlight_clf, subset=[c for c in ['f1_weighted', 'accuracy'] if c in clf_df.columns])
    st.dataframe(styled_clf, use_container_width=True)


    df_melt = clf_df.melt(id_vars='Run', value_vars=['accuracy', 'f1_weighted'], 
                          var_name='Metric', value_name='Score')
    
    fig_clf = px.line(df_melt, x='Run', y='Score', color='Metric', markers=True,
                      title='Model Performance Comparison',
                      color_discrete_sequence=['#2ecc71', '#3498db'])
    
    fig_clf.update_traces(marker_size=14, line_width=4)
    fig_clf.update_layout(
        yaxis_title="Score", 
        yaxis_range=[0.85, 1.02], 
        hovermode="x unified",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1}
    )
    
    st.plotly_chart(fig_clf, use_container_width=True)
else:
    st.warning("No classification runs found in MLflow.")

st.markdown("---")

# ── Regression ────────────────────────────────────────────────────────
st.subheader("🔵 Regression Models — Max Monthly EMI")
reg_df = get_runs("EMI_Regression")

if not reg_df.empty:
    reg_df = reg_df.sort_values('rmse').reset_index(drop=True)
    reg_df = reg_df.dropna(axis=1, how='all') # Drop 'None' columns (like classification metrics)
    
    # Apply Blue Bold to Lowest RMSE and Highest R2
    styled_reg = reg_df.style.apply(highlight_reg_min, subset=[c for c in ['rmse'] if c in reg_df.columns])\
                             .apply(highlight_reg_max, subset=[c for c in ['r2'] if c in reg_df.columns])
    st.dataframe(styled_reg, use_container_width=True)


    col3, col4 = st.columns(2)
    with col3:
        fig_rmse = px.area(reg_df, x='Run', y='rmse', markers=True, 
                           title='RMSE (Lower is Better)',
                           color_discrete_sequence=['#e67e22'])
        fig_rmse.update_traces(marker_size=12, line_width=3, fillcolor='rgba(230,126,34,0.15)')
        fig_rmse.update_layout(yaxis_title="RMSE (₹)", hovermode="x unified")
        st.plotly_chart(fig_rmse, use_container_width=True)

    with col4:
        fig_r2 = px.area(reg_df, x='Run', y='r2', markers=True, 
                         title='R² Score (Higher is Better)',
                         color_discrete_sequence=['#2ecc71'])
        fig_r2.update_traces(marker_size=12, line_width=3, fillcolor='rgba(46,204,113,0.15)')
        fig_r2.update_layout(yaxis_title="R² Score", yaxis_range=[0, 1.1], hovermode="x unified")
        st.plotly_chart(fig_r2, use_container_width=True)
else:
    st.warning("No regression runs found in MLflow.")

# ── Summary ───────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🥇 Best Model Summary")
col5, col6 = st.columns(2)
col5.success("**Best Classifier:** XGBoost\nAccuracy: 97.47% | F1: 0.9730")
col6.success("**Best Regressor:** XGBoost\nRMSE: ₹692 | R²: 0.9921")
