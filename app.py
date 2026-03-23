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
        st.write("### 🪄 Step-by-Step Prediction")
        st.write("Calculate EMI eligibility with our new guided 4-step wizard.")
        st.markdown("""
        - Simplified 4-step interface
        - Real-time risk factor analysis
        - Maximum EMI capacity prediction
        - Dynamic validation & feedback
        """)
    with col_b:
        st.write("### 🗂️ Applicant Management")
        st.write("A full CRM suite to track and manage historical predictions.")
        st.markdown("""
        - Save & review applicant records
        - Manual status overrides
        - Historical record directory
        - Full CRUD operations
        """)

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("### 🧠 Machine Learning Models")
        st.write("Powered by state-of-the-art ML algorithms for accurate predictions.")
        st.markdown("""
        - Dual model architecture
        - Classification + Regression
        - Continuous learning via MLflow
        - 97.4% High accuracy rates
        """)
    with col_b:
        st.write("### 💡 AI Advisor & Health Score")
        st.write("Get personalized financial health scores and diagnostics.")
        st.markdown("""
        - Custom action plans
        - Risk mitigation strategies
        - Credit improvement tips
        - Financial health guidance
        """)

with tab3:
    st.write("### 📈 Advanced Data Engineering")
    st.write("A professional toolkit for high-performance financial analysis.")
    col_a, col_b, col_c = st.columns(3)
    col_a.markdown("""
    <div class="feature-card-glass" style="--card-bg: rgba(239, 246, 255, 0.6); --card-border: rgba(191, 219, 254, 0.5); color: #1e40af;">
        <strong>🎯 Optimized Parquet</strong><br>
        <span style="font-size: 0.9rem;">Native support for Apache Parquet with 90% size reduction.</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_b.markdown("""
    <div class="feature-card-glass" style="--card-bg: rgba(240, 253, 244, 0.6); --card-border: rgba(187, 247, 208, 0.5); color: #166534;">
        <strong>🏆 Model Metrics</strong><br>
        <span style="font-size: 0.9rem;">Live MLflow tracking with static cloud fallback.</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_c.markdown("""
    <div class="feature-card-glass" style="--card-bg: rgba(254, 252, 232, 0.6); --card-border: rgba(254, 240, 138, 0.5); color: #854d0e;">
        <strong>🔍 Deep Insights</strong><br>
        <span style="font-size: 0.9rem;">Advanced EDA with correlation and distribution mappings.</span>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.write("### 🛡️ Security & Integrity")
    st.write("Your financial data is protected with local-first security measures.")
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("✅ Local-First Processing")
        st.success("✅ Zero Cloud Storage")
    with col_b:
        st.success("✅ Privacy Preserved")
        st.success("✅ Secure Model Hosting")

# ── Quick Start Guide ────────────────────────────────────────────────
with st.expander("🚀 Quick Start Guide — How to Use Phase 2"):
    st.markdown("""
    1. **🧙‍♂️ EMI Wizard** — Navigate through the 4-step flow to get your eligibility score.
    2. **💾 Save Record** — Click 'Save' at the end of the wizard to track the results.
    3. **🗂️ Management** — Head to the console to view, edit, or purge saved records.
    4. **📊 Insights & Metrics** — Explore the core dataset and model performance stats.
    """)

# ── System Status ─────────────────────────────────────────────────────
st.markdown("### 🔧 System Status")
sc1, sc2, sc3 = st.columns(3)
sc1.success("✅ Classification Model: Online")
sc2.success("✅ Regression Model: Online")
sc3.success("✅ Data Pipeline: Ready")

st.divider()
st.markdown("EMI Predict AI ✨ | Powered by Advanced AI 🧠")

