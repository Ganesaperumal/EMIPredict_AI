import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from styles import apply_glass_theme
from navigation import render_sidebar_nav

st.set_page_config(page_title="Data Insights", page_icon="📈", layout="wide")
apply_glass_theme()

# Custom Navigation
render_sidebar_nav("pages/Data_Insights.py")

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / 'data/cleaned/cleaned_emi_prediction_dataset.parquet'

st.markdown("""
<div class="glass-header" style="--header-bg: linear-gradient(135deg, rgba(238, 242, 254, 0.7), rgba(199, 210, 254, 0.7)); --header-border: rgba(255, 255, 255, 0.5);">
    <h1>📈 Data Insights</h1>
    <p>Exploratory analysis of 400,000 financial profiles</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        return pd.DataFrame()
    return pd.read_parquet(DATA_PATH)

df = load_data()

if df.empty:
    st.warning("No dataset found for analysis. Please ensure the preprocessing pipeline has run.")
else:
    # ── Map Categorical Labels ──────────────
    label_map = {0: 'Eligible', 1: 'High Risk', 2: 'Not Eligible'}
    if 'emi_eligibility' in df.columns and df['emi_eligibility'].dtype != 'object':
        df['emi_eligibility'] = df['emi_eligibility'].map(label_map)

    # ── Overview ─────────────────────────────────────────────────────────
    st.subheader("📋 Dataset Overview")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card-glass">Records: {len(df):,}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card-glass">Features: {df.shape[1]}</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card-glass">Scenarios: {df["emi_scenario"].nunique()}</div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card-glass">Avg Credit: {df["credit_score"].mean():.0f}</div>', unsafe_allow_html=True)

    st.dataframe(df.head(10), use_container_width=True)

    # ... (Rest of charts)
    st.write("Full visual analysis available below...")
    
    # ── Correlation Heatmap ───────────────────────────────────────────────
    st.subheader("🔥 Correlation Heatmap")
    num_df = df.select_dtypes(include='number').drop(columns=['max_monthly_emi'], errors='ignore')
    corr = num_df.corr().round(2)
    fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r')
    st.plotly_chart(fig, use_container_width=True)

st.stop() # Prevent any runaway Rendering
