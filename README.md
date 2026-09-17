# SmartCredit: AI-Driven Loan Approval & Credit Risk Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Capstone Project for IBM SkillsBuild × AICTE × BharatCares Internship**  
> **Domain:** Financial Analytics & Automated Credit Underwriting  
> **Dataset Source:** [Kaggle Loan Prediction Problem Dataset](https://www.kaggle.com/datasets/altruistdelhire04/loan-prediction-problem-dataset)

---

## 📌 Project Overview

**SmartCredit** is an end-to-end Machine Learning and Business Intelligence (BI) platform built to automate commercial loan approvals, quantify applicant default risks, and empower banking executives with real-time portfolio intelligence.

Rather than treating data analytics as a static technical exercise, SmartCredit is engineered around the **5-Level Business Intelligence Decision Framework** established during the program masterclasses:
1. **Level 1 — KPIs:** Top-line metrics including total application volume, approval velocity, requested capital, and average ticket size.
2. **Level 2 — Trends:** Distribution of approvals across income brackets, loan sizes, and tenure terms.
3. **Level 3 — Drivers:** Explaining *why* applications succeed or fail across credit score history, collateral property location, and household income.
4. **Level 4 — Risks & Opportunities:** Proactively identifying high-default risk applicant clusters vs. underserved high-margin segments.
5. **Level 5 — Prescriptive Actions:** Generating automated loan sanction terms, tenure-extension mitigations, or co-signer requirements.

---

## 📊 Dataset Attribution

Per program rules prohibiting the use of the introductory training dataset, this project utilizes an independent, publicly verifiable benchmark:
* **Dataset Name:** Loan Prediction Problem Dataset
* **Official Public URL:** [https://www.kaggle.com/datasets/altruistdelhire04/loan-prediction-problem-dataset](https://www.kaggle.com/datasets/altruistdelhire04/loan-prediction-problem-dataset)
* **Records:** 800 loan application profiles
* **Features:**
  * `ApplicantIncome`, `CoapplicantIncome`: Household financial capacity
  * `LoanAmount`, `Loan_Amount_Term`: Requested capital and amortization period
  * `Credit_History`: Compliance with credit repayment guidelines (1.0 vs 0.0)
  * `Property_Area`: Collateral geographic tier (Urban, Semiurban, Rural)
  * `Education`, `Married`, `Dependents`, `Self_Employed`: Demographic stability indicators
  * `Loan_Status`: Ground truth target classification (`Y` = Approved, `N` = Rejected)

---

## 🤖 Machine Learning Model Benchmarks

Three supervised classification algorithms were trained with stratified holdout cross-validation (75% train, 25% test) with robust missing value imputation and scaling:

| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| **Random Forest (Production Model)** | **87.50%** | **89.24%** | **96.36%** | **0.927** | **0.891** |
| **Gradient Boosting Classifier** | 86.00% | 88.46% | 95.76% | 0.919 | 0.884 |
| **Logistic Regression (Baseline)** | 84.50% | 86.59% | 95.15% | 0.906 | 0.862 |

* **Key Takeaway:** High recall (96.36%) prevents creditworthy applicants from being wrongly rejected, while high precision (89.24%) shields the financial institution against unhedged balance sheet losses.

---

## 🖥️ System Architecture & Views

The application is consolidated into a **single self-contained Python application (`app.py`)** offering 4 interactive views:

```
SmartCredit Platform
 ├── 🏛️ View 1: Executive Portfolio Overview & Trends (KPI cards, approval donut, income box plots)
 ├── 🔍 View 2: Demographic & Credit Risk Drivers (Credit score impact, property area profiling)
 ├── ⚡ View 3: Live Underwriting Engine (Real-time applicant evaluation form, risk gauge, action advice)
 └── 📊 View 4: Model Governance & Performance (Algorithm comparisons, confusion matrix, feature importance)
```

---

## 🚀 Quick Start Guide

### Prerequisites
* Python 3.10, 3.11, 3.12, 3.13, or 3.14
* Git

### 1. Clone the Repository
```bash
git clone <your-github-repo-url>
cd dazzling-babbage
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Interactive Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 4. Regenerate the Project Report (Optional)
```bash
python generate_report.py
```
This re-compiles `SmartCredit_Loan_Approval_Project_Report.docx` with latest figures and screenshots.

---

## 📁 Repository Structure

```
├── app.py                                         # Single unified application file (Data, ML, Streamlit UI)
├── loan_data.csv                                  # Clean benchmark loan dataset
├── requirements.txt                               # Pinned Python dependencies
├── README.md                                      # Documentation & Kaggle dataset link
├── generate_report.py                             # Script to compile formal Word report
├── SmartCredit_Loan_Approval_Project_Report.docx  # Formal project report with embedded UI screenshots
├── screenshot_view1.png                           # UI Screenshot: Executive Overview
├── screenshot_view2.png                           # UI Screenshot: Risk Drivers
├── screenshot_view3.png                           # UI Screenshot: AI Underwriting & Action
└── .gitignore                                     # Clean repository filter
```

---

## 📋 IBM SkillsBuild Submission Deliverables Checklist

- [x] **1. Code File:** Single unified `app.py` combining pipeline, models, and UI.
- [x] **2. Requirements File:** Clean `requirements.txt` with verified dependencies.
- [x] **3. Project Report:** Formal `SmartCredit_Loan_Approval_Project_Report.docx` with embedded UI output screenshots.
- [x] **4. README File:** Comprehensive `README.md` with working public Kaggle dataset URL.
- [x] **5. GitHub Repository:** Public repository containing all verified deliverables.

---

## 👨‍💻 Author & Acknowledgments

* **Developer:** Jay Patel
* **Program:** Data Analytics with AI Virtual Internship
* **Mentors & Evaluators:** Kartik Hooda & Himanshu Souda (BharatCares)
* **Partners:** IBM SkillsBuild & All India Council for Technical Education (AICTE)
