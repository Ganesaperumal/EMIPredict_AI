import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import joblib
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent / 'src'))
from styles import apply_glass_theme
from navigation import render_sidebar_nav

st.set_page_config(page_title="AI Financial Advisor", page_icon="🤖", layout="wide")
apply_glass_theme()

# Custom Navigation
render_sidebar_nav("pages/AI_Advisor.py")

@st.cache_resource
def load_models():
    PROJECT_ROOT = Path(__file__).parent.parent
    clf      = joblib.load(PROJECT_ROOT / 'models/best_classifier.pkl')
    reg      = joblib.load(PROJECT_ROOT / 'models/best_regressor.pkl')
    scaler   = joblib.load(PROJECT_ROOT / 'models/scaler.pkl')
    encoders = joblib.load(PROJECT_ROOT / 'models/encoders.pkl')
    return clf, reg, scaler, encoders


# ── Header ────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-header" style="--header-bg: linear-gradient(135deg, rgba(255, 241, 242, 0.7), rgba(254, 205, 211, 0.7)); --header-border: rgba(255, 255, 255, 0.5);">
    <h1>🤖 AI Financial Advisor</h1>
    <p>Personalized Financial Guidance & Recommendations</p>
</div>
""", unsafe_allow_html=True)

# ── 1. Determine View State ───────────────────────────────────────
# We no longer auto-load from CSV to ensure that the Calculator (1) 
# and Manual Form (3) follow strict precedence and fresh start rules.




col_h1, col_h2, col_h3 = st.columns(3)
col_h1.info("✨ Personalized")
col_h2.success("✅ Actionable")
col_h3.warning("🛡️ Privacy-first")




# ── 4 Tabs ────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Personalized Advice",
    "📚 General Tips",
    "💡 Best Practices",
    "📈 Financial Health"
])

# ════════════════════════════════════════════════════════════════════════
# TAB 1 — Personalized Advice
# ════════════════════════════════════════════════════════════════════════
with tab1:

    st.markdown("### 🎯 Your Personalized Recommendations")

    # ── 2. Determine View State ───────────────────────────────────────
    if 'last_prediction' not in st.session_state:
        # Show "No Data" Card
        col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
        with col_m2:
            with st.container(border=True):
                st.markdown("""
                <div class="tip-card-header" style="--tip-header-bg: linear-gradient(135deg, #800000, #4a0404); --tip-header-color: white; border-radius: 8px 8px 0 0; margin: -16px -16px 16px -16px; border-bottom: 2px solid #4a0404; text-align: center;">
                    <span>🤔</span> No Prediction Data Available
                </div>
                <div style="text-align: center; margin-top: 15px; margin-bottom: 15px; font-weight: 500;">
                    Complete the EMI Calculator first to receive personalized recommendations.
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("➜ Go to EMI Calculator", use_container_width=True):
                    st.switch_page("pages/EMI_Calculator.py")

        
        # Optional: Keep the manual form collapsed for better UX
        with st.expander("🛠️ Or Enter Details Manually", expanded=False):
            col1, col2, col3 = st.columns(3)
            m_income  = col1.number_input("Monthly Income (₹)", 10000, 500000, 50000, key="m_inc")
            m_emis    = col2.number_input("Total Monthly EMIs (₹)", 0, 300000, 10000, key="m_emi")
            c_score   = col3.slider("Credit Score", 300, 850, 650, key="c_scr")
            
            e_fund    = col1.number_input("Emergency Fund (₹)", 0, 2000000, 30000, key="e_fnd")
            m_savings = col2.number_input("Monthly Savings (₹)", 0, 200000, 5000, key="m_svg")
            m_balance = col3.number_input("Bank Balance (₹)", 0, 5000000, 150000, key="m_bal")
            
            m_req_amt = col1.number_input("Requested Loan (₹)", 10000, 5000000, 200000, key="m_req")
            m_tenure  = col2.slider("Tenure (months)", 3, 84, 24, key="m_ten")
            m_scenario = col3.selectbox("Loan Scenario", ["Personal Loan EMI", "Vehicle EMI", "Education EMI", "E-commerce Shopping EMI", "Home Appliances EMI"], key="m_sce")
            
            m_loans   = col1.selectbox("Any Existing Loans?", ["No", "Yes"], key="m_ex_ln")
            
            calc_manual = st.button("🔍 Generate Manual Advice", use_container_width=True)
            
            if calc_manual:
                clf, reg, scaler, encoders = load_models()
                
                # 1. Setup Data from Inputs & Realistic Defaults
                manual_data = {
                    'age': 35, 'gender': 'Male', 'marital_status': 'Married', 'education': 'Graduate',
                    'employment_type': 'Private', 'years_of_employment': 5, 'company_type': 'Medium',
                    'house_type': 'Own', 'family_size': 4, 'dependents': 1, 'monthly_rent': 0,
                    'school_fees': 0, 'college_fees': 0, 'travel_expenses': 2000, 
                    'groceries_utilities': 10000, 'other_monthly_expenses': 5000,
                }
                
                # Update with User's Manual Selections
                manual_data.update({
                    'monthly_salary': m_income,
                    'current_emi_amount': m_emis,
                    'credit_score': c_score,
                    'emergency_fund': e_fund,
                    'bank_balance': m_balance,
                    'requested_amount': m_req_amt,
                    'requested_tenure': m_tenure,
                    'emi_scenario': m_scenario,
                    'existing_loans': m_loans
                })
                
                # 2. Calculate Engineered Features (Using implied expenses from savings)
                # If User saves X and pays Y emi, their other expenses must be Income - X - Y
                implied_expenses = m_income - m_emis - m_savings
                total_exp = max(implied_expenses, 5000) # Floor at 5k for realism
                
                manual_data.update({
                    'total_monthly_expenses': total_exp + m_emis, # include the emi in total exp
                    'disposable_income': m_income - (total_exp + m_emis),
                    'emi_to_income_ratio': manual_data['requested_amount'] / (manual_data['monthly_salary'] * manual_data['requested_tenure'] + 1),
                    'savings_ratio': (manual_data['bank_balance'] + manual_data['emergency_fund']) / (manual_data['monthly_salary'] + 1),
                    'debt_burden': manual_data['current_emi_amount'] / (manual_data['monthly_salary'] + 1),
                    'family_pressure': manual_data['dependents'] / (manual_data['monthly_salary'] / 10000 + 1)
                })
                
                # 4. Feature Alignment (Exact 31 Columns)
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
                
                cat_cols = ['gender', 'marital_status', 'education', 'employment_type',
                            'company_type', 'house_type', 'emi_scenario', 'existing_loans']
                
                pd_raw = {}
                for col in FEATURE_COLS:
                    val = manual_data.get(col, 0)
                    if col in cat_cols:
                        try:
                            pd_raw[col] = encoders[col].transform([str(val)])[0]
                        except:
                            pd_raw[col] = 0
                    else:
                        pd_raw[col] = float(val) if val is not None else 0.0
                
                df_input = pd.DataFrame([pd_raw])[FEATURE_COLS]
                X_scaled = scaler.transform(df_input)
                
                # 5. Predict
                pred_class = clf.predict(X_scaled)[0]
                pred_emi = reg.predict(X_scaled)[0]
                label = encoders['emi_eligibility'].classes_[pred_class]
                
                # 6. Save to Session State
                st.session_state.last_prediction = {
                    'income': m_income,
                    'emis': m_emis,
                    'credit_score': c_score,
                    'emergency_fund': e_fund,
                    'eligibility': label,
                    'max_emi': float(pred_emi)
                }
                st.success("✅ Assessment generated successfully!")
                st.rerun()
    else:
        # ── Data-Driven Advice (Using session state) ───────────────────────
        data = st.session_state.last_prediction
        inc, emis, score, efund, elig, max_emi = (
            data['income'], data['emis'], data['credit_score'], 
            data['emergency_fund'], data['eligibility'], data['max_emi']
        )
        
        # 1. Eligibility Banner (Matches Screenshot)
        banner_colors = {
            "Eligible": ("#4db6ac", "🎉 ELIGIBLE FOR EMI", "Great! You qualify for loan approval"),
            "High_Risk": ("#f9a825", "⚠️ HIGH RISK WARNING", "Approval is possible but with stricter terms"),
            "Not_Eligible": ("#e57373", "🚨 NOT ELIGIBLE", "We recommend improving your profile before re-applying")
        }
        bg, title, sub = banner_colors.get(elig, banner_colors["High_Risk"])
        
        if elig == "Eligible":
            st.success(f"🎉 **ELIGIBLE FOR EMI**: {sub}")
        elif elig == "High_Risk":
            st.warning(f"⚠️ **HIGH RISK WARNING**: {sub}")
        else:
            st.error(f"🚨 **NOT ELIGIBLE**: {sub}")


        # 2. Dual Diagnostic Cards
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.write("#### ✅ What You're Doing Right")
            st.markdown(f"""
            - {"Strong financial profile" if elig=="Eligible" else "Manageable current expenses"}
            - {"Good credit management" if score > 700 else "Stable employment history"}
            - Stable income source
            - {"Manageable debt-to-income ratio" if (emis/inc < 0.35) else "Good bank balance buffer"}
            """)

        with col_c2:
            st.write("#### 💡 Optimization Tips")
            st.markdown(f"""
            - Maximum EMI: **₹{max_emi:,.2f}**
            - Stay within 80% of max EMI for comfort
            - Maintain emergency fund of 6+ months
            - {"Consider longer tenure for lower EMI" if elig!="Eligible" else "Avoid multiple simultaneous applications"}
            """)


        # 3. EMI Planning Calculator (Matches Screenshot)
        st.markdown("### 🧮 EMI Planning Calculator")
        with st.container(border=True):
            st.caption("**EMI Planning Guide**")
            
            plans = {
                "Maximum EMI (100%)": max_emi,
                "Recommended EMI (80%)": max_emi * 0.8,
                "Safe EMI (60%)": max_emi * 0.6
            }
            
            plan_df = pd.DataFrame({
                'Plan': list(plans.keys()),
                'Amount': list(plans.values()),
                'Color': ['#ef4444', '#3b82f6', '#10b981'] # Red, Blue, Green
            })
            
            
            fig_plan = go.Figure(go.Bar(
                x=plan_df['Amount'],
                y=plan_df['Plan'],
                orientation='h',
                marker_color=plan_df['Color'],
                text=[f"₹{v:,.0f}" for v in plan_df['Amount']],
                textposition='inside',
                insidetextanchor='end',
                textfont={'size': 12, 'color': 'white', 'family': 'Inter, sans-serif'}
            ))
            
            fig_plan.update_layout(
                margin={'l': 20, 'r': 20, 't': 20, 'b': 20},
                height=300,
                xaxis_title="Monthly EMI Amount (₹)",
                yaxis=dict(autorange="reversed"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis={'showgrid': True, 'gridcolor': 'rgba(0,0,0,0.05)'}
            )
            st.plotly_chart(fig_plan, use_container_width=True)

            # Bottom Recommendation Bar
            st.info(f"💡 Recommendation: Aim for EMI around ₹{max_emi*0.8:,.2f} for comfortable repayment")


        if st.button("🔄 Clear Results and Start Over", use_container_width=True):
            if 'last_prediction' in st.session_state:
                del st.session_state.last_prediction
            st.session_state.csv_autoload_done = True 
            st.rerun()





# ════════════════════════════════════════════════════════════════════════
# TAB 2 — General Tips
# ════════════════════════════════════════════════════════════════════════
with tab2:

    st.subheader("📚 General Financial Wisdom")


    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div class="tip-card" style="--tip-bg: #eff6ff; --tip-header-bg: #dbeafe; --tip-header-color: #1e40af; --tip-border: #bfdbfe;">
            <div class="tip-card-header">
                <span>🏦</span> EMI Management Rules
            </div>
            <div class="tip-card-body">
                <ul>
                    <li><b>50-30-20 Rule:</b> 50% needs, 30% wants, 20% savings</li>
                    <li><b>EMI Limit:</b> Keep total EMIs below 40% of income</li>
                    <li><b>Emergency Fund:</b> Maintain 6-12 months expenses</li>
                    <li><b>Credit Utilization:</b> Keep below 30% of limit</li>
                    <li><b>Diversification:</b> Don't put all eggs in one basket</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="tip-card" style="--tip-bg: #f0fdf4; --tip-header-bg: #dcfce7; --tip-header-color: #166534; --tip-border: #bbf7d0;">
            <div class="tip-card-header">
                <span>✅</span> Loan Application Tips
            </div>
            <div class="tip-card-body">
                <ul>
                    <li>Check credit score before applying</li>
                    <li>Compare interest rates across lenders</li>
                    <li>Read all terms and conditions</li>
                    <li>Calculate true cost including fees</li>
                    <li>Have all documents ready</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="tip-card" style="--tip-bg: #fff1f2; --tip-header-bg: #ffe4e6; --tip-header-color: #9f1239; --tip-border: #fecdd3;">
            <div class="tip-card-header">
                <span>⚠️</span> Red Flags to Avoid
            </div>
            <div class="tip-card-body">
                <ul>
                    <li>Taking loans for daily expenses</li>
                    <li>Multiple loan applications simultaneously</li>
                    <li>Ignoring loan terms and fine print</li>
                    <li>Missing EMI payment deadlines</li>
                    <li>Using credit card cash advances</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="tip-card" style="--tip-bg: #fefce8; --tip-header-bg: #fef9c3; --tip-header-color: #854d0e; --tip-border: #fef08a;">
            <div class="tip-card-header">
                <span>📈</span> Credit Score Boosters
            </div>
            <div class="tip-card-body">
                <ul>
                    <li>Pay all bills on time, every time</li>
                    <li>Keep old credit accounts active</li>
                    <li>Mix of credit types (secured + unsecured)</li>
                    <li>Dispute errors on credit report</li>
                    <li>Limit hard credit inquiries</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)





# ════════════════════════════════════════════════════════════════════════
# TAB 3 — Best Practices

# ════════════════════════════════════════════════════════════════════════
with tab3:

    st.subheader("💡 Best Practices for Financial Health")


    with st.expander("🏦 Debt to Income Ratio Management", expanded=True):
        st.markdown("""
        - **Target:** Keep below 40% of gross monthly income
        - **Calculation:** (Total Monthly Debt Payments / Gross Monthly Income) × 100
        - **Action:** If above 40%, prioritize debt reduction before new loans
        - **Impact:** Lower ratio = better loan approval chances
        """)

    with st.expander("💳 Credit Utilization Optimization"):
        st.markdown("""
        - **Target:** Use less than 30% of available credit
        - **Strategy:** Pay off balances multiple times per month
        - **Benefit:** Improves credit score quickly
        - **Monitoring:** Check credit reports quarterly
        """)

    with st.expander("🛡️ Emergency Fund Building"):
        st.markdown("""
        - **Goal:** 6-12 months of expenses
        - **Priority:** Build this BEFORE taking new loans
        - **Storage:** Keep in liquid, easily accessible account
        - **Usage:** Only for true emergencies
        """)

    with st.expander("📊 Expense Tracking"):
        st.markdown("""
        - **Method:** Use apps or spreadsheets
        - **Frequency:** Review weekly, analyze monthly
        - **Categories:** Housing, food, transport, entertainment, savings
        - **Optimization:** Cut 10% from top 3 expense categories
        """)

    with st.expander("📅 Loan Prepayment Strategy"):
        st.markdown("""
        - **When:** Prepay when you have surplus funds
        - **Priority:** Clear highest-interest loans first
        - **Benefit:** Saves significant interest over loan tenure
        - **Check:** Confirm no prepayment penalty before paying
        """)




# ════════════════════════════════════════════════════════════════════════

# TAB 4 — Financial Health
# ════════════════════════════════════════════════════════════════════════
with tab4:

    st.subheader("📈 Rate Your Financial Health")


    checks = {
        "Emergency fund covers 6+ months expenses": False,
        "Credit score above 750": False,
        "Total EMIs less than 40% of income": False,
        "Regular savings of 20%+ of income": False,
        "No missed payments in last 12 months": False,
        "Diversified income sources": False,
        "Insurance coverage adequate": False,
    }

    col1, col2, col3 = st.columns([0.75, 1, 1])

    with col1:
        checked_count = 0
        st.subheader("Check all that apply to you:")

        for label in checks:
            val = st.checkbox(label)
            if val:
                checked_count += 1
        score = int((checked_count / len(checks)) * 100)

    with col2:
        st.markdown("<h3 style='text-align: center;'>Financial Health Score</h3>", unsafe_allow_html=True)

        # ── Gauge Chart ───────────────────────────────────────────────────
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw={'projection': 'polar'})
        fig.patch.set_alpha(0) # Transparent
        fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

        # Exact screenshot colors
        colors = ['#e25822', '#f39c12', '#f1c40f', '#8dc63f', '#00a651']
        segments = [(0, 20, colors[0]), (20, 40, colors[1]), (40, 60, colors[2]), (60, 80, colors[3]), (80, 100, colors[4])]

        active_color = colors[0]
        for start, end, color in segments:
            if start <= score <= end or (score == 100 and end == 100):
                active_color = color
            
            gap = 0.5
            theta_start = ((start + (gap if start > 0 else 0)) / 100) * np.pi
            theta_end   = ((end - (gap if end < 100 else 0)) / 100) * np.pi
            theta = np.linspace(theta_start, theta_end, 100)
            ax.fill_between(theta, 0.70, 0.95, color=color, alpha=1.0, lw=0, zorder=2)

        theta_base = np.linspace(0, np.pi, 100)
        ax.fill_between(theta_base, 0, 0.25, color='#f1f5f9', alpha=1.0, lw=0, zorder=5)

        needle_angle = (score / 100) * np.pi
        ax.fill([needle_angle - 0.04, needle_angle, needle_angle + 0.04], 
                [0.1, 0.85, 0.1], color='#333333', zorder=4)

        ax.text(-0.02, 0.83, "0", ha='center', va='top', fontsize=12, fontweight='600', color='#9ca3af', zorder=3)
        ax.text(np.pi+0.01, 0.83, "100", ha='center', va='top', fontsize=12, fontweight='600', color='#9ca3af', zorder=3)

        ax.text(np.pi/2, 0.38, f"\n{int(score)}", ha='center', va='top',
                fontsize=20, fontweight='900', color=active_color, zorder=6)

        ax.set_ylim(0, 1.0)
        ax.set_theta_zero_location('W')
        ax.set_theta_direction(-1) 
        ax.set_thetamin(0)
        ax.set_thetamax(180)
        ax.axis('off')

        st.pyplot(fig, use_container_width=True)
        plt.close()

    with col3:
        with st.container():
            st.markdown(f"""
            <div class="metric-card-glass" style="--card-bg: linear-gradient(135deg, rgba(238, 242, 255, 0.7), rgba(199, 210, 254, 0.7)); --card-border: rgba(255, 255, 255, 0.5);">
                <div class="metric-label-glass">Health Score</div>
                <div class="metric-value-glass">{score}/100</div>
                <div class="metric-delta-glass"><span>🩺</span> Overall</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="metric-card-glass" style="--card-bg: linear-gradient(135deg, rgba(255, 241, 242, 0.7), rgba(254, 205, 211, 0.7)); --card-border: rgba(255, 255, 255, 0.5); margin-top: 1rem;">
                <div class="metric-label-glass">Tasks Completed</div>
                <div class="metric-value-glass">{checked_count}/{len(checks)}</div>
                <div class="metric-delta-glass"><span>✅</span> Progress</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        if score >= 85:
            st.success("🏆 Excellent! You are in a strong financial position.")
        elif score >= 65:
            st.info("👍 Good! A few improvements will make you even stronger.")
        elif score >= 40:
            st.warning("⚖️ Fair. Focus on building emergency fund and reducing debt")
        else:
            st.error("🚨 Needs attention. Prioritize financial stability before new loans.")
