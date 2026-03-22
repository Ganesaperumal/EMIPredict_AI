GLASS_CSS = """
<style>
/* Hiding all possible default navigation elements in the sidebar */
[data-testid="stSidebarNav"], 
.stSidebarNav, 
div[data-testid="stSidebarNavContents"] {
    display: none !important;
}

/* Page background image with white overlay for readability */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(255, 255, 255, 1), rgba(255, 255, 255, 1)), 
                url("https://images.pexels.com/photos/53594/blue-clouds-day-fluffy-53594.jpeg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background-color: rgba(255, 255, 255, 0.0);
}

.glass-header {
    background: var(--header-bg);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid var(--header-border);
    border-radius: 20px;
    padding: 1.2rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    width: 100%;
}
.glass-header h1 {
    font-size: 2.2rem !important;
    font-weight: 850 !important;
    margin: 0 !important;
    padding: 0 !important;
    color: #0f172a !important;
    letter-spacing: -0.02em !important;
    line-height: 1.2 !important;
}
.glass-header p {
    font-size: 1.05rem !important;
    margin: 0.3rem 0 0 0 !important;
    color: #475569 !important;
    font-weight: 600 !important;
}

.metric-card-glass {
    background: var(--card-bg);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 130px;
}
.metric-card-glass:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.2);
    border-color: rgba(255, 255, 255, 0.8);
}
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
    padding: 0.2rem 0.6rem !important;
    border-radius: 100px !important;
    background: rgba(16, 185, 129, 0.1) !important;
    color: #10b981 !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.2rem !important;
    margin-top: 0.4rem !important;
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


