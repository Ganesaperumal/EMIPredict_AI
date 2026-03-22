import streamlit as st

def render_sidebar_nav(current_page):
    # ── 1. Branded Header (Premium Liquid Glass) ───────────────────────────
    st.sidebar.markdown("""
        <div style="background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); 
                    border-radius: 18px; padding: 1.2rem; margin-bottom: 1.5rem; 
                    box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3); color: white;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="background: rgba(255,255,255,0.2); width: 42px; height: 42px; 
                            border-radius: 10px; display: flex; align-items: center; 
                            justify-content: center; font-size: 20px; font-weight: 800;">AI</div>
                <div>
                    <div style="font-weight: 800; font-size: 1.1rem; letter-spacing: -0.02em;">EMI Predict AI</div>
                    <div style="font-size: 0.75rem; opacity: 0.8; font-weight: 500;">Intelligent Risk Assessment</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── 2. Navigation Control ────────────────────────────────────────────────
    nav_pages = {
        "🏠 Dashboard": "app.py",
        "🧮 EMI Predictor": "pages/EMI_Calculator.py",
        "🗂️ Management": "pages/Management.py",
        "📈 Data Insights": "pages/Data_Insights.py",
        "🎡 Model Metrics": "pages/Model_Metrics.py",
        "🤖 AI Advisor": "pages/AI_Advisor.py"
    }
    
    options = list(nav_pages.keys())
    
    # Determine current selection based on filename
    default_index = 0
    current_filename = current_page.split('/')[-1]
    for i, (label, path) in enumerate(nav_pages.items()):
        if path.split('/')[-1] == current_filename:
            default_index = i
            break

    selection = st.sidebar.radio(
        "Navigation",
        options,
        index=default_index,
        label_visibility="visible"
    )
    
    # Check if a new page was selected
    if selection != options[default_index]:
        st.switch_page(nav_pages[selection])
    
    st.sidebar.markdown("---")

    # ── 3. System Status Badges ──────────────────────────────────────────────
    st.sidebar.markdown('<div style="font-weight: 700; font-size: 0.75rem; color: #64748b; margin-bottom: 10px; text-transform: uppercase;">✨ System Health</div>', unsafe_allow_html=True)
    
    badge_style = """
        <div style="display: flex; items-center; gap: 8px; background: {bg}; color: {fg}; 
                    padding: 6px 12px; border-radius: 10px; font-size: 0.75rem; font-weight: 600; margin-bottom: 6px;">
            <span>{icon}</span> {text}
        </div>
    """
    
    st.sidebar.markdown(badge_style.format(bg="#dcfce7", fg="#166534", icon="✅", text="System Online"), unsafe_allow_html=True)
    st.sidebar.markdown(badge_style.format(bg="#f0f9ff", fg="#075985", icon="🛡️", text="Privacy First"), unsafe_allow_html=True)
    st.sidebar.markdown(badge_style.format(bg="#fef3c7", fg="#92400e", icon="🚀", text="AI Optimized"), unsafe_allow_html=True)

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.caption("© 2026 EMIPredict AI Platform")