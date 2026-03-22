# 🏦 EMIPredict AI - Intelligent Financial Risk Assessment Platform

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![MLflow](https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=for-the-badge&logo=mlflow&logoColor=blue)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![XGBoost](https://img.shields.io/badge/XGBoost-blue?style=for-the-badge)

**EMIPredict AI** is a state-of-the-art financial risk assessment platform designed to automate and improve the accuracy of EMI (Equated Monthly Installment) eligibility and loan amount predictions. By leveraging high-performance machine learning models, the platform provides real-time insights for both lenders and applicants.

---

## 🚀 Key Features

- **🧙‍♂️ 4-Step EMI Wizard**: A guided, intuitive multi-step interface for predictive financial analysis.
- **🗂️ Applicant Management Console**: A full-featured CRM for tracking, editing, and managing historical applicant records.
- **📈 Data Insights Dashboard**: Interactive exploratory data analysis (EDA) of over 400,000 financial records across 5 diverse loan scenarios.
- **🎡 Model Performance Center**: Comprehensive metrics tracking via **MLflow**, featuring experiment comparisons and best-model highlighting.
- **🤖 AI Financial Advisor**: Personalized, actionable financial guidance based on individual risk profiles and health scores.
- **💎 Premium Liquid Glass UI**: A modern, Apple-style responsive interface with custom radial gradients and smooth transitions.

---

## 📊 Model Performance

| Objective | Model | Metric | Value |
| :--- | :--- | :--- | :--- |
| **Classification** | XGBoost | Accuracy | **97.47%** |
| | | F1-Score | **0.9730** |
| **Regression** | XGBoost | RMSE | **₹692** |
| | | R² Score | **0.9921** |

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/EMIPredict_AI.git
cd EMIPredict_AI
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### Launch the Application
```bash
streamlit run app.py
```

### Run Model Registration (Optional)
To update the local model registry with the latest best runs:
```bash
python src/register_models.py
```

---

## 📁 Project Structure

```text
EMIPredict_AI/
├── app.py                # Main application entry point
├── pages/                # Multi-page interface modules
├── models/               # Serialized model artifacts (.pkl)
├── src/                  # Core logic & design components
├── data/                 # Cleaned and processed datasets
├── mlruns/               # MLflow experiment tracking data
├── notebooks/            # Exploratory analysis notebooks
└── requirements.txt      # Project dependencies
```

---

## 🤝 Contribution

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

*Developed as part of an Intelligent Financial Risk Assessment initiative.*
