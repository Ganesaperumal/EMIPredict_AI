import streamlit as st
import pandas as pd
from pathlib import Path
import os
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from styles import apply_glass_theme
from navigation import render_sidebar_nav

st.set_page_config(page_title="Management Console", page_icon="🗂️", layout="wide")
apply_glass_theme()

# Custom Navigation
render_sidebar_nav("pages/Management.py")

PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / 'data/applicant_records.csv'

st.markdown("""
<div class="glass-header" style="--header-bg: linear-gradient(135deg, #fef3c7, #fde68a); --header-border: rgba(255, 255, 255, 0.5);">
    <h1>🗂️ Applicant Management Console</h1>
    <p>Track, review, and manage historical EMI predictions</p>
</div>
""", unsafe_allow_html=True)

def load_data():
    if not DB_PATH.exists():
        return pd.DataFrame(columns=['Date', 'Income', 'Requested', 'Status', 'Max_EMI'])
    try:
        df = pd.read_csv(DB_PATH)
        # Ensure it doesn't accidentally load the main dataset
        if len(df) > 1000: # Safety check
             return pd.DataFrame(columns=['Date', 'Income', 'Requested', 'Status', 'Max_EMI'])
        return df
    except:
        return pd.DataFrame(columns=['Date', 'Income', 'Requested', 'Status', 'Max_EMI'])

df = load_data()

if df.empty:
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; 
                padding: 4rem 2rem; background: rgba(255,255,255,0.4); border-radius: 24px; 
                border: 1px dashed rgba(15, 23, 42, 0.2); text-align: center; margin-top: 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem; filter: grayscale(1); opacity: 0.5;">📭</div>
        <h3 style="color: #64748b; margin-bottom: 0.5rem;">No Applicant Records Found</h3>
        <p style="color: #94a3b8; max-width: 400px; margin: 0 auto;">
            Predictions saved in the <b>EMI Predictor</b> wizard will appear here automatically for review and management.
        </p>
        <div style="margin-top: 2rem;">
            <a href="/EMI_Calculator" target="_self" style="text-decoration: none; background: #6366f1; 
               color: white; padding: 0.8rem 1.5rem; border-radius: 12px; font-weight: 600;">🧙‍♂️ Go to Predictor</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.subheader("📋 Saved Applications")
    st.dataframe(df, use_container_width=True)
    
    if st.button("🚨 Purge All Records"):
        if DB_PATH.exists():
            os.remove(DB_PATH)
            st.success("All records have been purged.")
            st.rerun()

st.stop() # Force stop to prevent any runaway rendering
