import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent / 'src'))
from styles import apply_glass_theme
from navigation import render_sidebar_nav

st.set_page_config(page_title="Data Insights", page_icon="📈", layout="wide")
apply_glass_theme()

# Custom Navigation
render_sidebar_nav("pages/Data_Insights.py")


st.markdown("""
<div class="glass-header" style="--header-bg: linear-gradient(135deg, rgba(238, 242, 255, 0.7), rgba(199, 210, 254, 0.7)); --header-border: rgba(255, 255, 255, 0.5);">
    <h1>📈 Data Insights</h1>
    <p>Exploratory analysis of 400,000 financial profiles</p>
</div>
""", unsafe_allow_html=True)





PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / 'data/cleaned/cleaned_emi_prediction_dataset.parquet'

@st.cache_data
def load_data():
    return pd.read_parquet(DATA_PATH)

df = load_data()

# ── Map Categorical Labels (Previously Encoded) ──────────────
# 0: Eligible, 1: High_Risk, 2: Not_Eligible (Alphabetical Order)
label_map = {0: 'Eligible', 1: 'High Risk', 2: 'Not Eligible'}
if df['emi_eligibility'].dtype != 'object':
    df['emi_eligibility'] = df['emi_eligibility'].map(label_map)

# ── Overview ─────────────────────────────────────────────────────────
st.subheader("📋 Dataset Overview")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-card-glass" style="--card-bg: linear-gradient(135deg, rgba(224, 242, 254, 0.7), rgba(186, 230, 253, 0.7)); --card-border: rgba(255, 255, 255, 0.5);">
        <div class="metric-label-glass">Total Records</div>
        <div class="metric-value-glass">{len(df):,}</div>
        <div class="metric-delta-glass"><span>📦</span> Dataset</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card-glass" style="--card-bg: linear-gradient(135deg, rgba(255, 241, 242, 0.7), rgba(254, 205, 211, 0.7)); --card-border: rgba(255, 255, 255, 0.5);">
        <div class="metric-label-glass">Features</div>
        <div class="metric-value-glass">{df.shape[1] - 2}</div>
        <div class="metric-delta-glass"><span>🔍</span> Variables</div>
    </div>
    """, unsafe_allow_html=True)


with c3:
    st.markdown(f"""
    <div class="metric-card-glass" style="--card-bg: linear-gradient(135deg, rgba(209, 250, 229, 0.7), rgba(110, 231, 183, 0.7)); --card-border: rgba(255, 255, 255, 0.5);">
        <div class="metric-label-glass">EMI Scenarios</div>
        <div class="metric-value-glass">{df['emi_scenario'].nunique()}</div>
        <div class="metric-delta-glass"><span>🎯</span> Scenarios</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card-glass" style="--card-bg: linear-gradient(135deg, rgba(238, 242, 255, 0.7), rgba(199, 210, 254, 0.7)); --card-border: rgba(255, 255, 255, 0.5);">
        <div class="metric-label-glass">Avg Credit Score</div>
        <div class="metric-value-glass">{df['credit_score'].mean():.0f}</div>
        <div class="metric-delta-glass"><span>🏆</span> Average</div>
    </div>
    """, unsafe_allow_html=True)
st.divider()

st.dataframe(df.head(10), use_container_width=True)

df_sample = df.sample(n=5000, random_state=42) # Safe sample for heavy browser plots

# ── Target Distribution ───────────────────────────────────────────────
st.subheader("🎯 Target Variable Distributions")
col1, col2 = st.columns(2)

with col1:
    counts = df['emi_eligibility'].value_counts().reset_index()
    counts.columns = ['Eligibility', 'Count']
    fig1 = px.pie(counts, values='Count', names='Eligibility', hole=0.4,
                  title='EMI Eligibility Breakdown',
                  color='Eligibility',
                  color_discrete_map={'Eligible': '#2ecc71', 'Not_Eligible': '#e74c3c', 'High Risk': '#f39c12'})
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.violin(df_sample, y='max_monthly_emi', box=True, points="all",
                     title='Max Monthly EMI Spread (Sampled)',
                     color_discrete_sequence=['#3498db'])
    st.plotly_chart(fig2, use_container_width=True)

# ── Feature Relationships (Replacing boring baseline) ────────────────
st.subheader("💡 Income vs Requested Amount by Eligibility")
fig3 = px.scatter(df_sample, x='monthly_salary', y='requested_amount', 
                  color='emi_eligibility', opacity=0.6,
                  title="How Monthly Salary impacts Requested Loan Amount",
                  color_discrete_map={'Eligible': '#2ecc71', 'Not Eligible': '#e74c3c', 'High Risk': '#f39c12'},
                  labels={'monthly_salary': 'Monthly Salary (₹)', 'requested_amount': 'Requested Amount (₹)'})
st.plotly_chart(fig3, use_container_width=True)

# ── Numeric Distributions ─────────────────────────────────────────────
st.subheader("📈 Key Financial Feature Distributions (Box Plots)")
num_cols = ['monthly_salary', 'bank_balance', 'emergency_fund', 'requested_amount']
fig4 = go.Figure()
for col in num_cols:
    fig4.add_trace(go.Box(y=df_sample[col], name=col.replace('_', ' ').title()))
fig4.update_layout(title="Distribution Spreads across Key Financial Features",
                   yaxis_title="Value (Varies by Unit)", showlegend=False)
st.plotly_chart(fig4, use_container_width=True)

# ── Correlation Heatmap ───────────────────────────────────────────────
st.subheader("🔥 Correlation Heatmap")
num_df = df.select_dtypes(include='number').drop(columns=['max_monthly_emi'], errors='ignore')
corr = num_df.corr().round(2)
text_matrix = corr.map(lambda x: '' if x == 0 else str(x))

fig5 = px.imshow(corr, 
                 text_auto=True, 
                 aspect="auto", 
                 color_continuous_scale='RdBu_r', # Red-Blue diverging scale
                 color_continuous_midpoint=0,
                 title="Feature Correlation Matrix (Inter-relationships)")

fig5.update_layout(
    width=1200, 
    height=800, 
    xaxis_tickangle=-45,
    margin=dict(l=100, r=100, t=100, b=100)
)
st.plotly_chart(fig5, use_container_width=True)

# ── Radar Risk Profiler ───────────────────────────────────────────
st.subheader("🕸️ Financial Risk Profiles (Radar Chart)")
radar_cols = ['monthly_salary', 'bank_balance', 'emergency_fund', 'requested_amount', 'current_emi_amount']
radar_df = df.groupby('emi_eligibility')[radar_cols].mean().reset_index()

# Normalize columns 0-1 for radar plotting
for col in radar_cols:
    c_min, c_max = df[col].min(), df[col].max()
    radar_df[col] = (radar_df[col] - c_min) / (c_max - c_min)

radar_melt = radar_df.melt(id_vars='emi_eligibility', var_name='Metric', value_name='Normalized Score')
radar_melt['Metric'] = radar_melt['Metric'].str.replace('_', ' ').str.title()

fig6 = px.line_polar(radar_melt, r='Normalized Score', theta='Metric', color='emi_eligibility', line_close=True,
                     title='Average Traits: Eligible vs High Risk vs Not Eligible',
                     color_discrete_map={'Eligible': '#2ecc71', 'High Risk': '#f39c12', 'Not Eligible': '#e74c3c'})
fig6.update_traces(fill='toself', opacity=0.7)
fig6.update_layout(polar=dict(radialaxis=dict(visible=False)), margin=dict(t=50, b=50))
st.plotly_chart(fig6, use_container_width=True)

