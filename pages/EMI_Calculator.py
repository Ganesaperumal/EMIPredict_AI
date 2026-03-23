import streamlit as st
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent / 'src'))
from styles import apply_glass_theme
from navigation import render_sidebar_nav

st.set_page_config(page_title="EMI Prediction", page_icon="🧮", layout="wide")
apply_glass_theme()

# Custom Navigation
render_sidebar_nav("pages/EMI_Calculator.py")



PROJECT_ROOT = Path(__file__).parent.parent

@st.cache_resource
def load_models():
    clf   = joblib.load(PROJECT_ROOT / 'models/best_classifier.pkl')
    reg   = joblib.load(PROJECT_ROOT / 'models/best_regressor.pkl')
    scaler   = joblib.load(PROJECT_ROOT / 'models/scaler.pkl')
    encoders = joblib.load(PROJECT_ROOT / 'models/encoders.pkl')
    return clf, reg, scaler, encoders

clf, reg, scaler, encoders = load_models()

# ── Wizard Logic ──────────────────────────────────────────────────────
if 'calc_step' not in st.session_state:
    st.session_state.calc_step = 1
if 'calc_data' not in st.session_state:
    st.session_state.calc_data = {}

def next_step(): st.session_state.calc_step += 1
def prev_step(): st.session_state.calc_step -= 1
def reset_wizard():
    st.session_state.calc_step = 1
    st.session_state.calc_data = {}

st.markdown("""
<div class="glass-header" style="--header-bg: linear-gradient(135deg, #e0f2fe, #bae6fd); --header-border: rgba(255, 255, 255, 0.5);">
    <h1>🧮 EMI Smart Predictor</h1>
    <p>Complete the 4-step assessment for your instant eligibility report</p>
</div>
""", unsafe_allow_html=True)

# ── Progress Tracker ──────────────────────────────────────────────────
steps = [
    ("👤", "Personal"),
    ("💼", "Employment"),
    ("💰", "Financial"),
    ("🎯", "Results")
]

cols = st.columns(len(steps))
for i, (icon, label) in enumerate(steps):
    step_num = i + 1
    is_active = st.session_state.calc_step == step_num
    is_done = st.session_state.calc_step > step_num
    
    status_class = "step-active" if is_active else ("step-done" if is_done else "")
    cols[i].markdown(f"""
        <div class="step-item {status_class}">
            <div class="step-dot">{icon if not is_done else '✓'}</div>
            <div class="step-label">{label}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── STEP 1: Personal Info ─────────────────────────────────────────────
if st.session_state.calc_step == 1:
    with st.form("step1"):
        st.subheader("👤 Personal Background")
        c1, c2 = st.columns(2)
        age = c1.slider("Age", 25, 60, st.session_state.calc_data.get('age', 35))
        gender = c2.selectbox("Gender", ["Male", "Female"], index=0 if st.session_state.calc_data.get('gender') == 'Male' else (1 if st.session_state.calc_data.get('gender') == 'Female' else 0))
        marital = c1.selectbox("Marital Status", ["Single", "Married"], index=0 if st.session_state.calc_data.get('marital_status') == 'Single' else (1 if st.session_state.calc_data.get('marital_status') == 'Married' else 0))
        education = c2.selectbox("Education", ["High School", "Graduate", "Post Graduate", "Professional"])
        house = c1.selectbox("House Type", ["Rented", "Own", "Family"])
        family = c2.slider("Family Size", 1, 10, st.session_state.calc_data.get('family_size', 4))
        deps = c1.slider("Dependents", 0, 6, st.session_state.calc_data.get('dependents', 1))
        
        if st.form_submit_button("Continue to Employment 💼", use_container_width=True):
            st.session_state.calc_data.update({
                'age': age, 'gender': gender, 'marital_status': marital, 
                'education': education, 'house_type': house, 
                'family_size': family, 'dependents': deps
            })
            next_step()
            st.rerun()

# ── STEP 2: Employment ────────────────────────────────────────────────
elif st.session_state.calc_step == 2:
    with st.form("step2"):
        st.subheader("💼 Employment Details")
        c1, c2 = st.columns(2)
        emp_type = c1.selectbox("Employment Type", ["Private", "Government", "Self-employed"])
        comp_type = c2.selectbox("Company Type", ["Large", "Medium", "Small", "Startup"])
        exp = c1.slider("Years of Employment", 0, 35, st.session_state.calc_data.get('years_of_employment', 5))
        salary = c2.number_input("Monthly Salary (₹)", 15000, 200000, st.session_state.calc_data.get('monthly_salary', 50000), step=1000)
        
        col_back, col_next = st.columns([1, 2])
        if col_back.form_submit_button("← Back"):
            prev_step()
            st.rerun()
        if col_next.form_submit_button("Continue to Financials 💰", use_container_width=True):
            st.session_state.calc_data.update({
                'employment_type': emp_type, 'company_type': comp_type,
                'years_of_employment': exp, 'monthly_salary': salary
            })
            next_step()
            st.rerun()

# ── STEP 3: Financial & Loan ──────────────────────────────────────────
elif st.session_state.calc_step == 3:
    with st.form("step3"):
        st.subheader("💰 Financial Capacity & Request")
        c1, c2, c3 = st.columns(3)
        balance = c1.number_input("Bank Balance (₹)", 0, 5000000, 100000)
        emergency = c2.number_input("Emergency Fund (₹)", 0, 2000000, 50000)
        credit = c3.slider("Credit Score", 300, 850, 650)
        
        loans = c1.selectbox("Existing Loans", ["Yes", "No"])
        current_emi = c2.number_input("Current EMI (₹)", 0, 100000, 0)
        scenario = c3.selectbox("EMI Scenario", ["E-commerce Shopping EMI", "Home Appliances EMI", "Vehicle EMI", "Personal Loan EMI", "Education EMI"])
        
        req_amt = c1.number_input("Requested Amount (₹)", 10000, 1500000, 200000)
        tenure = c2.slider("Tenure (months)", 3, 84, 24)

        st.divider()
        st.subheader("🏠 Monthly Expenses")
        e1, e2, e3 = st.columns(3)
        rent = e1.number_input("Rent (₹)", 0, 100000, 10000)
        school = e2.number_input("School Fees (₹)", 0, 50000, 0)
        travel = e3.number_input("Travel (₹)", 0, 30000, 3000)
        groceries = e1.number_input("Groceries (₹)", 0, 50000, 8000)
        other = e2.number_input("Other (₹)", 0, 50000, 2000)
        
        col_back, col_next = st.columns([1, 2])
        if col_back.form_submit_button("← Back"):
            prev_step()
            st.rerun()
        if col_next.form_submit_button("🔮 Generate Prediction", use_container_width=True):
            st.session_state.calc_data.update({
                'bank_balance': balance, 'emergency_fund': emergency, 'credit_score': credit,
                'existing_loans': loans, 'current_emi_amount': current_emi, 'emi_scenario': scenario,
                'requested_amount': req_amt, 'requested_tenure': tenure, 'monthly_rent': rent,
                'school_fees': school, 'travel_expenses': travel, 'groceries_utilities': groceries,
                'other_monthly_expenses': other, 'college_fees': 0
            })
            next_step()
            st.rerun()

# ── STEP 4: Results ───────────────────────────────────────────────────
elif st.session_state.calc_step == 4:
    data = st.session_state.calc_data
    # Feature Engineering
    total_exp = data['monthly_rent'] + data['school_fees'] + data.get('college_fees', 0) + \
                data['travel_expenses'] + data['groceries_utilities'] + \
                data['other_monthly_expenses'] + data['current_emi_amount']
    
    disposable = data['monthly_salary'] - total_exp
    emi_to_inc = data['requested_amount'] / (data['monthly_salary'] * data['requested_tenure'] + 1)
    savings_rat = (data['bank_balance'] + data['emergency_fund']) / (data['monthly_salary'] + 1)
    debt_burden = data['current_emi_amount'] / (data['monthly_salary'] + 1)
    family_pres = data['dependents'] / (data['monthly_salary'] / 10000 + 1)

    # Prepare for Prediction
    raw = data.copy()
    raw.update({
        'total_monthly_expenses': total_exp, 'disposable_income': disposable,
        'emi_to_income_ratio': emi_to_inc, 'savings_ratio': savings_rat,
        'debt_burden': debt_burden, 'family_pressure': family_pres
    })

    cat_cols = ['gender', 'marital_status', 'education', 'employment_type',
                'company_type', 'house_type', 'emi_scenario', 'existing_loans']
    
    # ── Feature Alignment ──────────────────────────────────────────
    # The scaler expects columns in the exact order they were trained
    FEATURE_COLS = [
        'age', 'gender', 'marital_status', 'education', 'monthly_salary', 
        'employment_type', 'years_of_employment', 'company_type', 'house_type', 
        'monthly_rent', 'family_size', 'dependents', 'school_fees', 'college_fees', 
        'travel_expenses', 'groceries_utilities', 'other_monthly_expenses', 
        'existing_loans', 'current_emi_amount', 'credit_score', 'bank_balance', 
        'emergency_fund', 'emi_scenario', 'requested_amount', 'requested_tenure', 
        'total_monthly_expenses', 'disposable_income', 'emi_to_income_ratio', 
        'savings_ratio', 'debt_burden', 'family_pressure'
    ]

    # Apply Encoding
    pd_raw = {}
    for col in FEATURE_COLS:
        val = raw.get(col, 0) # Default to 0 if missing
        if col in cat_cols:
            try:
                pd_raw[col] = encoders[col].transform([str(val)])[0]
            except:
                pd_raw[col] = 0
        else:
            pd_raw[col] = float(val) if val is not None else 0.0

    df_input = pd.DataFrame([pd_raw])[FEATURE_COLS] # Reorder to match training!

    X_scaled = scaler.transform(df_input)
    pred_class = clf.predict(X_scaled)[0]
    pred_proba = clf.predict_proba(X_scaled)[0]
    pred_emi = reg.predict(X_scaled)[0]

    label = encoders['emi_eligibility'].classes_[pred_class]
    
    # UI Results
    st.subheader("📊 Assessment Report")
    r1, r2 = st.columns(2)
    
    indicators = {"Eligible": "✅", "High_Risk": "⚠️", "Not_Eligible": "🚨"}
    colors = {"Eligible": "#dcfce7", "High_Risk": "#fef3c7", "Not_Eligible": "#fee2e2"}
    text_colors = {"Eligible": "#166534", "High_Risk": "#92400e", "Not_Eligible": "#991b1b"}
    
    res_label = label.replace('_', ' ')
    r1.markdown(f"""
        <div style="background: {colors[label]}; border-radius: 16px; padding: 2rem; text-align: center; border: 1px solid rgba(0,0,0,0.05);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{indicators[label]}</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: {text_colors[label]}">{res_label.upper()}</div>
            <div style="font-size: 0.9rem; opacity: 0.8; color: {text_colors[label]}">AI Risk Assessment Result</div>
        </div>
    """, unsafe_allow_html=True)

    if label == "Not_Eligible":
        r2.markdown(f"""
            <div style="background: #fff1f2; border-radius: 16px; padding: 2rem; text-align: center; border: 1px solid rgba(0,0,0,0.05); height: 100%;">
                <div style="font-size: 0.9rem; font-weight: 700; color: #9f1239; text-transform: uppercase;">Next Steps</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #be123c; margin: 1rem 0;">Improve Your Profile</div>
                <div style="font-size: 0.85rem; color: #e11d48; line-height: 1.4;">
                    Based on our AI analysis, your current financial risk is too high. 
                    Consider reducing existing debts or increasing your down payment.
                </div>
                <a href="AI_Advisor" target="_self" style="display: inline-block; margin-top: 1rem; color: #be123c; font-weight: 700; text-decoration: none; font-size: 0.8rem; border: 1px solid #be123c; padding: 4px 12px; border-radius: 20px;">View AI Advice →</a>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Show Safe EMI for Eligible and High Risk
        r2.markdown(f"""
            <div style="background: #f0f9ff; border-radius: 16px; padding: 2rem; text-align: center; border: 1px solid rgba(0,0,0,0.05); height: 100%;">
                <div style="font-size: 0.9rem; font-weight: 700; color: #075985; text-transform: uppercase;">Maximum Safe EMI</div>
                <div style="font-size: 3.5rem; font-weight: 900; color: #0369a1; margin: 0.5rem 0;">₹{pred_emi:,.0f}</div>
                <div style="font-size: 0.8rem; color: #0c4a6e;">Recommended monthly capacity</div>
                <div style="font-size: 0.7rem; color: #0369a1; opacity: 0.6; margin-top: 0.5rem;">
                    { '⚠️ Exercise caution while borrowing' if label == 'High_Risk' else '✅ Safe to proceed with this amount' }
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.write("**Confidence Breakdown:**")
    for i, lbl in enumerate(encoders['emi_eligibility'].classes_):
        st.progress(float(pred_proba[i]), text=f"{lbl}: {pred_proba[i]*100:.1f}%")

    # SAVE TO DATABASE (Phase 2 Feature)
    if st.button("💾 Save Applicant Record to Management Console"):
        import os
        from datetime import datetime
        db_path = PROJECT_ROOT / 'data/applicant_records.csv'
        record = {
            'Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'Income': data['monthly_salary'],
            'Requested': data['requested_amount'],
            'Status': label,
            'Max_EMI': pred_emi
        }
        df_rec = pd.DataFrame([record])
        if not db_path.exists():
            df_rec.to_csv(db_path, index=False)
        else:
            df_rec.to_csv(db_path, mode='a', header=False, index=False)
        st.toast("✅ Record saved successfully!", icon="🗂️")

    st.divider()
    if st.button("♻️ Start New Assessment"):
        reset_wizard()
        st.rerun()
