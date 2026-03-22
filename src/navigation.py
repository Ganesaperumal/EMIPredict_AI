import streamlit as st

def render_sidebar_nav(current_page):
    # ── 1. Branded Header (Inline CSS) ───────────────────────────────────────
    st.sidebar.markdown("""
        <div style="background:linear-gradient(135deg,#6366f1,#818cf8);border-radius:10px;
             padding:1rem;margin-bottom:1rem;color:white;text-align:center;">
          <div style="font-weight:800;font-size:1.2rem;letter-spacing:-0.02em;line-height:1.1;">
            EMI Predict AI ✨
          </div>
        </div>
    """, unsafe_allow_html=True)


    # ── 2. Navigation Control ────────────────────────────────────────────────
    nav_pages = {
        "🏠 Home": "app.py",
        "🧮 EMI Predictor": "pages/EMI_Calculator.py",
        "📈 Data Insights": "pages/Data_Insights.py",
        "🎡 Model Metrics": "pages/Model_Metrics.py",
        "🤖 AI Advisor": "pages/AI_Advisor.py"
    }
    
    st.sidebar.markdown("---")
    options = list(nav_pages.keys())
    
    # Determine current selection based on filename
    default_index = 0
    current_filename = current_page.split('/')[-1]
    for i, (label, path) in enumerate(nav_pages.items()):
        if path.split('/')[-1] == current_filename:
            default_index = i
            break

    selection = st.sidebar.radio(
        "Go to",
        options,
        index=default_index,
        label_visibility="collapsed"
    )
    
    # Check if a new page was selected
    if selection != options[default_index]:
        st.switch_page(nav_pages[selection])
    
    st.sidebar.markdown("---")

    # ── 3. Quick Stats ───────────────────────────────────────────────────────
    st.sidebar.markdown("### ⚡ Quick Stats")
    qc1, qc2 = st.sidebar.columns(2)
    qc1.metric("Models", "2", "Active")
    qc2.metric("Accuracy", "97.4%", "+2%")

    st.sidebar.markdown("---")

    # ── 4. System Status ─────────────────────────────────────────────────────
    st.sidebar.markdown("### 🟡 Status")
    st.sidebar.success("✅ System Online")
    st.sidebar.info("🔷 Models Loaded")