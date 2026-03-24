import streamlit as st
import pandas as pd
from pathlib import Path
import os
import sys
from datetime import datetime

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
    return pd.read_csv(DB_PATH)

def save_data(df):
    df.to_csv(DB_PATH, index=False)

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
        <div style="margin-top: 1rem;"></div>
    """, unsafe_allow_html=True)
    if st.button("🧙‍♂️ Go to Predictor", use_container_width=True):
        st.switch_page("pages/EMI_Calculator.py")
else:
    # ── Quick Analytics ──────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Applications", len(df))
    eligible_count = len(df[df['Status'] == 'Eligible'])
    col2.metric("Eligible Applicants", eligible_count)
    col3.metric("System Load", "Optimal", "✅")

    st.markdown("<br>", unsafe_allow_html=True)
    
    tab_view, tab_edit, tab_admin = st.tabs(["📋 View Directory", "✏️ Edit Records", "🗑️ Admin Tools"])

    with tab_view:
        st.subheader("Applicant Directory")
        # Search & Filter
        f1, f2 = st.columns(2)
        search = f1.text_input("Search (by Index or Date)", placeholder="Type to filter...")
        status_filter = f2.selectbox("Filter by Status", ["All", "Eligible", "High_Risk", "Not_Eligible"])
        
        view_df = df.copy()
        if status_filter != "All":
            view_df = view_df[view_df['Status'] == status_filter]
        
        # Display as cards for premium feel
        for i, row in view_df.iterrows():
            status_color = "#10b981" if row['Status'] == 'Eligible' else ("#f59e0b" if row['Status'] == 'High_Risk' else "#ef4444")
            st.markdown(f"""
                <div class="mgmt-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-weight: 800; color: #6366f1;">ID #{i}</span> 
                            <span style="color: #64748b; font-size: 0.8rem; margin-left: 10px;">🕒 {row['Date']}</span>
                        </div>
                        <div style="background: {status_color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;">
                            {row['Status'].upper()}
                        </div>
                    </div>
                    <div style="display: flex; gap: 40px; margin-top: 15px;">
                        <div>
                            <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Applicant Income</div>
                            <div style="font-size: 1.1rem; font-weight: 700;">₹{row['Income']:,.0f}</div>
                        </div>
                        <div>
                            <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Requested Loan</div>
                            <div style="font-size: 1.1rem; font-weight: 700;">₹{row['Requested']:,.0f}</div>
                        </div>
                        <div>
                            <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Max Safe EMI</div>
                            <div style="font-size: 1.1rem; font-weight: 700; color: #0ea5e9;">₹{row['Max_EMI']:,.0f}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with tab_edit:
        st.subheader("Manual Record Override")
        edit_id = st.selectbox("Select Record ID to Modify", df.index)
        if edit_id is not None:
            curr_row = df.iloc[edit_id]
            with st.form("edit_applicant"):
                new_status = st.selectbox("Override Status", ["Eligible", "High_Risk", "Not_Eligible"], 
                                         index=["Eligible", "High_Risk", "Not_Eligible"].index(curr_row['Status']))
                new_income = st.number_input("Adjust Income", value=float(curr_row['Income']))
                
                if st.form_submit_button("Update Record 💾"):
                    df.at[edit_id, 'Status'] = new_status
                    df.at[edit_id, 'Income'] = new_income
                    save_data(df)
                    st.success(f"Record #{edit_id} updated successfully!")
                    st.rerun()

    with tab_admin:
        st.subheader("Database Maintenance")
        st.warning("These actions are permanent and cannot be undone.")
        
        del_id = st.number_input("Delete specific ID", min_value=0, max_value=len(df)-1, step=1)
        if st.button("🗑️ Delete Selected Record", type="primary"):
            df = df.drop(df.index[del_id])
            save_data(df)
            st.success(f"Record #{del_id} deleted.")
            st.rerun()
            
        st.markdown("---")
        if st.button("🚨 Purge All Records"):
            if DB_PATH.exists():
                os.remove(DB_PATH)
                st.success("All records have been purged from the system.")
                st.rerun()
