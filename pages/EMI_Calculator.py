import streamlit as st
import pickle
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
    clf   = pickle.load(open(PROJECT_ROOT / 'models/best_classifier.pkl', 'rb'))
    reg   = pickle.load(open(PROJECT_ROOT / 'models/best_regressor.pkl', 'rb'))
    scaler   = pickle.load(open(PROJECT_ROOT / 'models/scaler.pkl', 'rb'))
    encoders = pickle.load(open(PROJECT_ROOT / 'models/encoders.pkl', 'rb'))
    return clf, reg, scaler, encoders

clf, reg, scaler, encoders = load_models()

st.markdown("""
<div class="glass-header" style="--header-bg: linear-gradient(135deg, rgba(209, 250, 229, 0.7), rgba(110, 231, 183, 0.7)); --header-border: rgba(255, 255, 255, 0.5);">
    <h1>🧮 EMI Eligibility Prediction</h1>
    <p>Fill in the applicant details to get real-time predictions</p>
</div>
""", unsafe_allow_html=True)





with st.form("prediction_form"):
    st.subheader("👤 Personal Details")
    c1, c2, c3 = st.columns(3)
    age            = c1.slider("Age", 25, 60, 35)
    gender         = c2.selectbox("Gender", ["Male", "Female"])
    marital_status = c3.selectbox("Marital Status", ["Single", "Married"])
    education      = c1.selectbox("Education", ["High School", "Graduate", "Post Graduate", "Professional"])
    employment_type= c2.selectbox("Employment Type", ["Private", "Government", "Self-employed"])
    company_type   = c3.selectbox("Company Type", ["Large", "Medium", "Small", "Startup"])
    house_type     = c1.selectbox("House Type", ["Rented", "Own", "Family"])
    family_size    = c2.slider("Family Size", 1, 10, 4)
    dependents     = c3.slider("Dependents", 0, 6, 1)
    years_of_employment = c1.slider("Years of Employment", 0, 35, 5)

    st.subheader("💰 Financial Details")
    c4, c5, c6 = st.columns(3)
    monthly_salary  = c4.number_input("Monthly Salary (₹)", 15000, 200000, 50000, step=1000)
    bank_balance    = c5.number_input("Bank Balance (₹)", 0, 5000000, 100000, step=10000)
    emergency_fund  = c6.number_input("Emergency Fund (₹)", 0, 2000000, 50000, step=5000)
    credit_score    = c4.slider("Credit Score", 300, 850, 650)
    existing_loans  = c5.selectbox("Existing Loans", ["Yes", "No"])
    current_emi_amount = c6.number_input("Current EMI (₹)", 0, 100000, 0, step=500)

    st.subheader("🏠 Monthly Expenses")
    c7, c8, c9 = st.columns(3)
    monthly_rent       = c7.number_input("Monthly Rent (₹)", 0, 100000, 10000, step=500)
    school_fees        = c8.number_input("School Fees (₹)", 0, 50000, 0, step=500)
    college_fees       = c9.number_input("College Fees (₹)", 0, 50000, 0, step=500)
    travel_expenses    = c7.number_input("Travel Expenses (₹)", 0, 30000, 3000, step=500)
    groceries_utilities= c8.number_input("Groceries & Utilities (₹)", 0, 50000, 8000, step=500)
    other_monthly_expenses = c9.number_input("Other Expenses (₹)", 0, 50000, 2000, step=500)

    st.subheader("📋 Loan Request")
    c10, c11, c12 = st.columns(3)
    emi_scenario     = c10.selectbox("EMI Scenario", ["E-commerce Shopping EMI", "Home Appliances EMI", "Vehicle EMI", "Personal Loan EMI", "Education EMI"])
    requested_amount = c11.number_input("Requested Amount (₹)", 10000, 1500000, 200000, step=10000)
    requested_tenure = c12.slider("Tenure (months)", 3, 84, 24)

    submitted = st.form_submit_button("🔮 Predict Now", use_container_width=True)

if submitted:
    # Feature Engineering (must match preprocessing.py)
    total_exp = monthly_rent + school_fees + college_fees + travel_expenses + groceries_utilities + other_monthly_expenses + current_emi_amount
    disposable  = monthly_salary - total_exp
    emi_to_inc  = requested_amount / (monthly_salary * requested_tenure + 1)
    savings_rat = (bank_balance + emergency_fund) / (monthly_salary + 1)
    debt_burden = current_emi_amount / (monthly_salary + 1)
    family_pres = dependents / (monthly_salary / 10000 + 1)

    raw = {
        'age': age, 'gender': gender, 'marital_status': marital_status,
        'education': education, 'monthly_salary': monthly_salary,
        'employment_type': employment_type, 'years_of_employment': years_of_employment,
        'company_type': company_type, 'house_type': house_type,
        'monthly_rent': monthly_rent, 'family_size': family_size,
        'dependents': dependents, 'school_fees': school_fees,
        'college_fees': college_fees, 'travel_expenses': travel_expenses,
        'groceries_utilities': groceries_utilities, 'other_monthly_expenses': other_monthly_expenses,
        'existing_loans': existing_loans, 'current_emi_amount': current_emi_amount,
        'credit_score': credit_score, 'bank_balance': bank_balance,
        'emergency_fund': emergency_fund, 'emi_scenario': emi_scenario,
        'requested_amount': requested_amount, 'requested_tenure': requested_tenure,
        'total_monthly_expenses': total_exp, 'disposable_income': disposable,
        'emi_to_income_ratio': emi_to_inc, 'savings_ratio': savings_rat,
        'debt_burden': debt_burden, 'family_pressure': family_pres
    }

    cat_cols = ['gender', 'marital_status', 'education', 'employment_type',
                'company_type', 'house_type', 'emi_scenario', 'existing_loans']
    for col in cat_cols:
        try:
            raw[col] = encoders[col].transform([raw[col]])[0]
        except ValueError:
            raw[col] = 0

    df_input = pd.DataFrame([raw])
    X_scaled = scaler.transform(df_input)

    pred_class = clf.predict(X_scaled)[0]
    pred_proba = clf.predict_proba(X_scaled)[0]
    pred_emi   = reg.predict(X_scaled)[0]

    class_labels = encoders['emi_eligibility'].classes_
    label = class_labels[pred_class]

    # Store in session state for AI Advisor
    st.session_state.last_prediction = {
        'income': monthly_salary,
        'emis': current_emi_amount,
        'credit_score': credit_score,
        'emergency_fund': emergency_fund,
        'bank_balance': bank_balance,
        'eligibility': label,
        'max_emi': pred_emi
    }

    st.markdown("---")
    st.subheader("📊 Prediction Results")

    col_a, col_b = st.columns(2)
    # Eligibility Indicator Logic
    indicators = {"Eligible": "✅ ", "High_Risk": "⚠️ ", "Not_Eligible": "🚨 "}
    display_label = f"{indicators.get(label, '')}{label.replace('_', ' ')}"
    
    with col_a:
        st.metric("EMI Eligibility", display_label)

    with col_b:
        st.metric("Max Safe EMI", f"₹{pred_emi:,.0f}")


    st.write("**Confidence Scores:**")
    for i, lbl in enumerate(class_labels):
        st.progress(float(pred_proba[i]), text=f"{lbl}: {pred_proba[i]*100:.1f}%")
