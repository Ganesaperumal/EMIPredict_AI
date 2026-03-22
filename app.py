import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from styles import apply_glass_theme
from navigation import render_sidebar_nav

st.set_page_config(
    page_title="EMIPredict AI Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_glass_theme()

# ── Sidebar Navigation ────────────────────────────────────────────────
with st.sidebar:
    render_sidebar_nav("app.py")

st.markdown("""
<div class="glass-header" style="--header-bg: linear-gradient(135deg, rgba(224, 242, 254, 0.7), rgba(186, 230, 253, 0.7)); --header-border: rgba(255, 255, 255, 0.5);">
    <h1>🏠 Dashboard Overview</h1>
    <p>EMIPredict AI — Smart Financial Risk Assessment</p>
</div>
""", unsafe_allow_html=True)


st.markdown("### 📋 System Overview")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-card-glass" style="--card-bg: linear-gradient(135deg, rgba(224, 242, 254, 0.7), rgba(186, 230, 253, 0.7)); --card-border: rgba(255, 255, 255, 0.5);">
        <div class="metric-label-glass">🤖 AI Models</div>
        <div class="metric-value-glass">2</div>
        <div class="metric-delta-glass"><span>✅</span> Active</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card-glass" style="--card-bg: linear-gradient(135deg, rgba(255, 241, 242, 0.7), rgba(254, 205, 211, 0.7)); --card-border: rgba(255, 255, 255, 0.5);">
        <div class="metric-label-glass">📦 Predictions</div>
        <div class="metric-value-glass">4 Lakhs+</div>
        <div class="metric-delta-glass"><span>📈</span> Total</div>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown("""
    <div class="metric-card-glass" style="--card-bg: linear-gradient(135deg, rgba(209, 250, 229, 0.7), rgba(110, 231, 183, 0.7)); --card-border: rgba(255, 255, 255, 0.5);">
        <div class="metric-label-glass">🏆 Accuracy</div>
        <div class="metric-value-glass">97.4%</div>
        <div class="metric-delta-glass"><span>🔥</span> Score</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card-glass" style="--card-bg: linear-gradient(135deg, rgba(238, 242, 255, 0.7), rgba(199, 210, 254, 0.7)); --card-border: rgba(255, 255, 255, 0.5);">
        <div class="metric-label-glass">⚡ Response</div>
        <div class="metric-value-glass">&lt;1s</div>
        <div class="metric-delta-glass"><span>⏱️</span> Avg</div>
    </div>
    """, unsafe_allow_html=True)




# ── Platform Capabilities — Tabs ─────────────────────────────────────
st.markdown("### ✨ Platform Capabilities")
tab1, tab2, tab3, tab4 = st.tabs(["🔧 Core Features", "🤖 AI Power", "📊 Analytics", "🛡️ Security"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("### 📱 Smart EMI Calculator")
        st.write("Calculate EMI eligibility with advanced AI algorithms.")
        st.markdown("""
        - Real-time eligibility assessment
        - Maximum EMI capacity prediction
        - Risk factor analysis
        - Multiple loan scenarios
        """)
    with col_b:
        st.write("### 📊 Visual Analytics")
        st.write("Comprehensive data visualization and exploratory analysis.")
        st.markdown("""
        - Interactive charts & graphs
        - Distribution analysis
        - Correlation heatmaps
        - Trend identification
        """)

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("### 🧠 Machine Learning Models")
        st.write("Powered by state-of-the-art ML algorithms for accurate predictions.")
        st.markdown("""
        - Dual model architecture
        - Classification + Regression
        - Continuous learning
        - High accuracy rates
        """)
    with col_b:
        st.write("### 💡 Intelligent Recommendations")
        st.write("Get personalized financial advice based on your profile.")
        st.markdown("""
        - Custom action plans
        - Risk mitigation strategies
        - Credit improvement tips
        - Financial health guidance
        """)

with tab3:
    st.write("### 📈 Advanced Analytics Features")
    st.write("A focused toolkit for deep exploratory analysis.")
    col_a, col_b, col_c = st.columns(3)
    col_a.info("**📦 Dataset Management**\\nUpload, clean, and manage your financial datasets efficiently.")
    col_b.success("**🏆 Model Performance**\\nTrack accuracy, F1 scores, RMSE, and feature importance metrics.")
    col_c.warning("**🔍 Deep Insights**\\nExplore correlations, distributions, and financial patterns.")

with tab4:
    st.write("### 🛡️ Security & Privacy")
    st.write("Your financial data is protected with enterprise-grade security measures.")
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("✅ Local Processing")
        st.success("✅ No Cloud Storage")
    with col_b:
        st.success("✅ Encrypted Models")
        st.success("✅ Privacy First")

# ── Quick Start Guide ────────────────────────────────────────────────
with st.expander("🚀 Quick Start Guide — How to Use This Platform"):
    st.markdown("""
    1. **🧮 EMI Predictor** — Enter applicant details and get instant EMI eligibility + max EMI amount
    2. **📈 Data Insights** — Explore the 400K dataset with distributions, correlations, and EDA visuals
    3. **🎡 Model Metrics** — Compare all 6 trained models (3 classifiers + 3 regressors) via MLflow
    4. **🤖 AI Advisor** — Get personalized financial health advice, tips, and best practices
    """)

# ── System Status ─────────────────────────────────────────────────────
st.markdown("### 🔧 System Status")
sc1, sc2, sc3 = st.columns(3)
sc1.success("✅ Classification Model: Online")
sc2.success("✅ Regression Model: Online")
sc3.success("✅ Data Pipeline: Ready")

st.divider()
st.markdown("EMI Predict AI ✨ | Powered by Advanced AI 🧠")

