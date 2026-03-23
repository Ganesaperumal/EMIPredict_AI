import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os
from pathlib import Path    

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent


def clean_data(df):
    # 1. Age: Handle mixed formats like 38.0.0
    df['age'] = pd.to_numeric(df['age'].astype(str).str.split('.').str[0], errors='coerce')
    df['age'] = df['age'].fillna(df['age'].median())
    
    # 2. Gender: Standardize M/F/Male/Female
    df['gender'] = df['gender'].str[0].str.upper().map({'M': 'Male', 'F': 'Female'})
    df['gender'] = df['gender'].fillna('Male')
    
    # 3. Education: Impute with mode
    if 'education' in df.columns:
        df['education'] = df['education'].fillna(df['education'].mode()[0])
    
    # 4. Monthly Salary: Handle mixed numeric formats
    df['monthly_salary'] = pd.to_numeric(df['monthly_salary'].astype(str).str.split('.').str[0], errors='coerce')
    df['monthly_salary'] = df['monthly_salary'].fillna(df['monthly_salary'].median())
    
    # 5. Monthly Rent: Smart imputation (Median for Rented, 0 for others)
    rent_median = df[df['house_type'] == 'Rented']['monthly_rent'].median()
    df.loc[(df['house_type'] == 'Rented') & (df['monthly_rent'].isna()), 'monthly_rent'] = rent_median
    df['monthly_rent'] = df['monthly_rent'].fillna(0)
    
    # 6. Bank Balance: Numeric cleaning
    df['bank_balance'] = pd.to_numeric(df['bank_balance'].astype(str).str.split('.').str[0], errors='coerce')
    df['bank_balance'] = df['bank_balance'].fillna(df['bank_balance'].median())
    
    # 7. Credit Score & Emergency Fund
    df['credit_score'] = df['credit_score'].fillna(df['credit_score'].median())
    df['emergency_fund'] = df['emergency_fund'].fillna(0)
    
    return df


def load_and_engineer(path=os.path.join(project_root, "data/raw/emi_prediction_dataset.csv")):
    if path.endswith('.csv'):
        df = pd.read_csv(path, low_memory=False)
    else:
        df = pd.read_parquet(path)

    # ── Advanced Cleaning ─────────────────────────────────────────────
    df = clean_data(df)

    # ── Feature Engineering ──────────────────────────────────────────
    # 1. Total monthly expenses
    expense_cols = ['monthly_rent', 'school_fees', 'college_fees',
                    'travel_expenses', 'groceries_utilities',
                    'other_monthly_expenses', 'current_emi_amount']
    df['total_monthly_expenses'] = df[expense_cols].fillna(0).sum(axis=1)

    # 2. Disposable income
    df['disposable_income'] = df['monthly_salary'] - df['total_monthly_expenses']

    # 3. EMI-to-income ratio (requested)
    df['emi_to_income_ratio'] = df['requested_amount'] / (df['monthly_salary'] * df['requested_tenure'])

    # 4. Savings ratio
    df['savings_ratio'] = (df['bank_balance'] + df['emergency_fund'].fillna(0)) / (df['monthly_salary'] + 1)

    # 5. Debt burden (existing EMI / salary)
    df['debt_burden'] = df['current_emi_amount'].fillna(0) / (df['monthly_salary'] + 1)

    # 6. Family financial pressure
    df['family_pressure'] = df['dependents'] / (df['monthly_salary'] / 10000 + 1)

    print(f"Features after engineering: {df.shape[1]} columns")

    # ── Encoding ─────────────────────────────────────────────────────
    cat_cols = ['gender', 'marital_status', 'education', 'employment_type',
                'company_type', 'house_type', 'emi_scenario', 'existing_loans']

    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    # ── Targets ──────────────────────────────────────────────────────
    target_clf = 'emi_eligibility'
    target_reg = 'max_monthly_emi'

    le_target = LabelEncoder()
    df[target_clf] = le_target.fit_transform(df[target_clf].astype(str))
    encoders['emi_eligibility'] = le_target
    print("Target classes:", le_target.classes_)

    # ── Save production copy for App ───────────────────────────────
    prod_path = project_root / 'data/cleaned/cleaned_emi_prediction_dataset.parquet'
    prod_path.parent.mkdir(exist_ok=True)
    df.to_parquet(prod_path, index=False)
    print(f"Production dataset refreshed at {prod_path}")

    # ── Split features ───────────────────────────────────────────────
    drop_cols = [target_clf, target_reg]
    X = df.drop(columns=drop_cols)
    y_clf = df[target_clf]
    y_reg = df[target_reg]

    # ── Train/Test Split ─────────────────────────────────────────────
    X_train, X_test, yc_train, yc_test, yr_train, yr_test = train_test_split(
        X, y_clf, y_reg, test_size=0.2, random_state=42, stratify=y_clf
    )

    # ── Scaling ──────────────────────────────────────────────────────
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ── Save artifacts ───────────────────────────────────────────────
    models_dir = project_root / 'models'
    models_dir.mkdir(exist_ok=True)
    pickle.dump(scaler, open(models_dir / 'scaler.pkl', 'wb'))
    pickle.dump(encoders, open(models_dir / 'encoders.pkl', 'wb'))
    print(f"Scaler and encoders saved to {models_dir}/")

    print(f"\nTrain size: {X_train.shape}, Test size: {X_test.shape}")

    return X_train_scaled, X_test_scaled, yc_train, yc_test, yr_train, yr_test, X_train.columns.tolist()


if __name__ == '__main__':
    load_and_engineer()
