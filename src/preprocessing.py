import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os
from pathlib import Path    

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent


def load_and_engineer(path=os.path.join(project_root, "data/cleaned/cleaned_emi_prediction_dataset.parquet")):
    df = pd.read_parquet(path)

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
