GLASS_CSS = """
<style>
/* Hiding all possible default navigation elements in the sidebar */
[data-testid="stSidebarNav"], 
.stSidebarNav, 
div[data-testid="stSidebarNavContents"] {
    display: none !important;
}

/* Main App Container - Apple-style subtle radial overlay */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    background-image: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.05) 0, transparent 50%), 
                      radial-gradient(at 50% 0%, rgba(168, 85, 247, 0.05) 0, transparent 50%), 
                      radial-gradient(at 100% 0%, rgba(14, 165, 233, 0.05) 0, transparent 50%);
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background-color: transparent;
}

/* Glass Header - More "Liquid" with higher blur */
.glass-header {
    background: var(--header-bg);
    backdrop-filter: blur(25px) saturate(180%);
    -webkit-backdrop-filter: blur(25px) saturate(180%);
    border: 1px solid var(--header-border);
    border-radius: 24px;
    padding: 1.5rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.1);
}

.glass-header h1 {
    font-size: 2.5rem !important;
    font-weight: 850 !important;
    color: #1e293b !important;
    letter-spacing: -0.03em !important;
}

/* Metric Cards - Enhanced with Hover Transforms */
.metric-card-glass {
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--card-border);
    border-radius: 22px;
    padding: 1.25rem;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 4px 20px -5px rgba(0, 0, 0, 0.05);
}

.metric-card-glass:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.15);
}

/* Wizard Step Tracker Styles */
.step-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2.5rem;
    padding: 0 1rem;
}
.step-item {
    text-align: center;
    flex: 1;
    position: relative;
}
.step-dot {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    margin: 0 auto 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    transition: all 0.3s ease;
}
.step-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #64748b;
}
.step-active .step-dot {
    background: linear-gradient(135deg, #dbeafe, #bfdbfe); /* Lighter Blue */
    color: #1e40af;
    box-shadow: 0 0 15px rgba(191, 219, 254, 0.5);
    border: 2px solid #60a5fa;
}
.step-active .step-label { color: #1e40af; font-weight: 700; }
.step-done .step-dot { background: #10b981; color: white; }
.step-done .step-label { color: #10b981; }

/* Management Content Cards */
.mgmt-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}
.mgmt-card:hover { border-color: #6366f1; box-shadow: 0 4px 12px rgba(99,102,241,0.1); }
.metric-label-glass {
    font-size: 0.8rem !important;
    font-weight: 750 !important;
    color: #475569 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-bottom: 0.3rem !important;
}
.metric-value-glass {
    font-size: 2.2rem !important;
    font-weight: 900 !important;
    color: #0f172a !important;
    line-height: 1 !important;
    margin: 0.1rem 0 !important;
    letter-spacing: -0.04em !important;
}
.metric-delta-glass {
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    padding: 0.2rem 0.8rem !important;
    border-radius: 100px !important;
    background: rgba(16, 185, 129, 0.1) !important;
    color: #10b981 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important; /* Centered */
    gap: 0.4rem !important;
    margin-top: 0.6rem !important;
}
.tip-card {
    background: var(--tip-bg);
    border: 1px solid var(--tip-border);
    border-radius: 12px;
    margin-bottom: 1.5rem;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
.tip-card-header {
    background: var(--tip-header-bg);
    padding: 0.8rem 1.2rem;
    color: var(--tip-header-color, white);
    font-weight: 700;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    border-bottom: 1px solid var(--tip-border);
}
.tip-card-body {
    padding: 1.2rem;
    color: #334155;
    line-height: 1.6;
}
.tip-card-body ul {
    margin: 0;
    padding-left: 1.2rem;
}
.tip-card-body li {
    margin-bottom: 0.5rem;
}

</style>




"""



def apply_glass_theme():
    import streamlit as st
    # Custom CSS to hide default navigation
    st.markdown(GLASS_CSS, unsafe_allow_html=True)


