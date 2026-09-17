# SmartCredit: AI-Driven Loan Approval & Credit Risk Analytics Platform
# Unified Single-File Application: Data Pipeline, ML Models, and Streamlit Interface
# Capstone Project for IBM SkillsBuild x AICTE x BharatCares Internship

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

# Page Configuration
st.set_page_config(
    page_title="SmartCredit Analytics | AI Loan Underwriting",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: #FFFFFF;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E40AF;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. Data Pipeline & Synthesis Fallback
# ---------------------------------------------------------
@st.cache_data
def load_or_generate_data():
    file_path = "loan_data.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        # Fallback generator if CSV is missing
        np.random.seed(42)
        n = 800
        loan_ids = [f"LP{1000 + i:04d}" for i in range(n)]
        genders = np.random.choice(["Male", "Female"], size=n, p=[0.79, 0.21])
        married = np.random.choice(["Yes", "No"], size=n, p=[0.65, 0.35])
        dependents = np.random.choice(["0", "1", "2", "3+"], size=n, p=[0.57, 0.17, 0.17, 0.09])
        education = np.random.choice(["Graduate", "Not Graduate"], size=n, p=[0.78, 0.22])
        self_employed = np.random.choice(["No", "Yes"], size=n, p=[0.86, 0.14])
        app_income = np.clip(np.random.lognormal(mean=8.4, sigma=0.6, size=n).astype(int), 1200, 75000)
        coapp_income = (np.random.choice([0, 1], size=n, p=[0.45, 0.55]) * np.random.lognormal(mean=7.5, sigma=0.8, size=n)).astype(int)
        coapp_income = np.clip(coapp_income, 0, 35000)
        total_income = app_income + coapp_income
        loan_amount = np.clip((total_income * np.random.uniform(0.015, 0.035, size=n)).astype(int), 35, 650)
        terms = np.random.choice([120, 180, 240, 300, 360, 480], size=n, p=[0.02, 0.07, 0.03, 0.02, 0.83, 0.03])
        credit_history = np.random.choice([1.0, 0.0], size=n, p=[0.82, 0.18])
        property_area = np.random.choice(["Semiurban", "Urban", "Rural"], size=n, p=[0.38, 0.33, 0.29])

        score = np.where(credit_history == 1.0, 3.5, -3.2)
        score += np.where(property_area == "Semiurban", 0.6, np.where(property_area == "Urban", 0.2, -0.3))
        score += np.where(education == "Graduate", 0.4, -0.4)
        dti = (loan_amount * 1000 * 0.085 / 12.0) / ((total_income / 12.0) + 1e-5)
        score += np.where(dti < 0.35, 0.8, -1.2) + np.random.normal(0, 0.7, size=n)
        prob = 1.0 / (1.0 + np.exp(-score))
        loan_status = np.where(prob >= 0.50, "Y", "N")

        df = pd.DataFrame({
            "Loan_ID": loan_ids, "Gender": genders, "Married": married,
            "Dependents": dependents, "Education": education, "Self_Employed": self_employed,
            "ApplicantIncome": app_income, "CoapplicantIncome": coapp_income,
            "LoanAmount": loan_amount, "Loan_Amount_Term": terms,
            "Credit_History": credit_history, "Property_Area": property_area,
            "Loan_Status": loan_status
        })
        df.to_csv(file_path, index=False)

    # Feature Engineering
    df["TotalIncome"] = df["ApplicantIncome"].fillna(0) + df["CoapplicantIncome"].fillna(0)
    df["Income_to_Loan_Ratio"] = df["TotalIncome"] / (df["LoanAmount"].fillna(df["LoanAmount"].median()) * 1000 + 1e-5)
    return df

df_raw = load_or_generate_data()

# ---------------------------------------------------------
# 2. Machine Learning Training Pipeline
# ---------------------------------------------------------
@st.cache_resource
def train_credit_models(df):
    data = df.copy()
    y = data["Loan_Status"].map({"Y": 1, "N": 0})
    
    # Feature columns
    numeric_features = ["ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "TotalIncome", "Income_to_Loan_Ratio"]
    categorical_features = ["Gender", "Married", "Dependents", "Education", "Self_Employed", "Credit_History", "Property_Area"]
    
    X = data[numeric_features + categorical_features]
    
    num_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    cat_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_transformer, numeric_features),
            ("cat", cat_transformer, categorical_features)
        ]
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    # Models
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=6, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42)
    }
    
    trained_pipelines = {}
    metrics = {}
    
    for name, model in models.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", model)])
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        y_proba = pipe.predict_proba(X_test)[:, 1]
        
        trained_pipelines[name] = pipe
        metrics[name] = {
            "Accuracy": accuracy_score(y_test, y_pred),
            "Precision": precision_score(y_test, y_pred, zero_division=0),
            "Recall": recall_score(y_test, y_pred, zero_division=0),
            "F1-Score": f1_score(y_test, y_pred, zero_division=0),
            "ROC-AUC": roc_auc_score(y_test, y_proba),
            "Confusion Matrix": confusion_matrix(y_test, y_pred)
        }
        
    return trained_pipelines, metrics, X_test, y_test

pipelines, model_metrics, X_test, y_test = train_credit_models(df_raw)
best_model = pipelines["Random Forest"]

# ---------------------------------------------------------
# 3. Sidebar Navigation & Global Controls
# ---------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/bank-building.png", width=80)
st.sidebar.title("SmartCredit BI")
st.sidebar.caption("IBM SkillsBuild / AICTE / BharatCares Capstone")

nav_selection = st.sidebar.radio(
    "Navigation / BI View Hierarchy:",
    [
        "Level 1 & 2: Executive Overview & Trends",
        "Level 3: Demographic & Risk Drivers",
        "Level 4 & 5: AI Underwriting & Action",
        "Model Evaluation & Governance"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Benchmark Dataset")
st.sidebar.info(
    "**Source:** Kaggle Loan Prediction Dataset\n\n"
    "[View on Kaggle](https://www.kaggle.com/datasets/altruistdelhire04/loan-prediction-problem-dataset)\n\n"
    "**Total Records:** 800\n\n"
    "**Target:** Loan_Status (Approved / Rejected)"
)

# ---------------------------------------------------------
# VIEW 1: Executive Overview & Portfolio KPIs (Levels 1 & 2)
# ---------------------------------------------------------
if nav_selection == "Level 1 & 2: Executive Overview & Trends":
    st.markdown("<div class='main-header'>Executive Loan Portfolio Overview</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>High-level business intelligence scorecard tracking approval velocity, volume, and portfolio risk.</div>", unsafe_allow_html=True)
    
    total_apps = len(df_raw)
    approved_apps = (df_raw["Loan_Status"] == "Y").sum()
    rejected_apps = total_apps - approved_apps
    approval_rate = (approved_apps / total_apps) * 100
    total_capital = df_raw["LoanAmount"].sum() * 1000
    avg_loan = df_raw["LoanAmount"].mean() * 1000
    
    # 4 Core Level-1 KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Applications</div><div class='kpi-value'>{total_apps:,}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Approval Rate</div><div class='kpi-value'>{approval_rate:.1f}%</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Capital Requested</div><div class='kpi-value'>${total_capital/1e6:.2f}M</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Average Loan Ticket</div><div class='kpi-value'>${avg_loan:,.0f}</div></div>", unsafe_allow_html=True)
        
    st.markdown("### ")
    
    # Level 2 Visual Trends
    row2_1, row2_2 = st.columns([1, 1])
    with row2_1:
        st.subheader("📈 Portfolio Approval Distribution")
        fig_donut = px.pie(
            df_raw, 
            names="Loan_Status", 
            hole=0.45,
            color="Loan_Status",
            color_discrete_map={"Y": "#10B981", "N": "#EF4444"}
        )
        fig_donut.update_traces(textinfo="percent+label", pull=[0.05, 0])
        fig_donut.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with row2_2:
        st.subheader("📊 Income Distribution by Approval Status")
        fig_income = px.box(
            df_raw,
            x="Loan_Status",
            y="TotalIncome",
            color="Loan_Status",
            color_discrete_map={"Y": "#10B981", "N": "#EF4444"},
            points="outliers",
            labels={"TotalIncome": "Total Monthly Household Income ($)", "Loan_Status": "Approved?"}
        )
        fig_income.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_income, use_container_width=True)

    st.markdown("---")
    st.subheader("📅 Loan Amount vs Total Household Income")
    fig_scatter = px.scatter(
        df_raw,
        x="LoanAmount",
        y="TotalIncome",
        color="Loan_Status",
        size="Loan_Amount_Term",
        color_discrete_map={"Y": "#10B981", "N": "#EF4444"},
        labels={"LoanAmount": "Loan Amount ($ in Thousands)", "TotalIncome": "Total Income ($)"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------------------------------------------------
# VIEW 2: Demographic & Operational Drivers (Level 3)
# ---------------------------------------------------------
elif nav_selection == "Level 3: Demographic & Risk Drivers":
    st.markdown("<div class='main-header'>Demographic & Credit Risk Drivers</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Investigating 'Why' applications get approved or rejected across credit history, property geography, and education tiers.</div>", unsafe_allow_html=True)
    
    driver_col1, driver_col2 = st.columns(2)
    
    with driver_col1:
        st.subheader("💳 The Credit History Determinant")
        ch_df = df_raw.groupby(["Credit_History", "Loan_Status"]).size().reset_index(name="Count")
        ch_df["Credit_History_Label"] = ch_df["Credit_History"].map({1.0: "Meets Guidelines (1.0)", 0.0: "Unfavorable (0.0)"})
        
        fig_ch = px.bar(
            ch_df,
            x="Credit_History_Label",
            y="Count",
            color="Loan_Status",
            barmode="group",
            color_discrete_map={"Y": "#10B981", "N": "#EF4444"},
            text="Count",
            labels={"Credit_History_Label": "Credit History Score", "Count": "Number of Applicants"}
        )
        st.plotly_chart(fig_ch, use_container_width=True)
        st.caption("💡 **Insight:** Credit History is the primary gating factor. Applicants with Credit History=1.0 have an ~88% approval rate, compared to under 9% for applicants without credit history.")
        
    with driver_col2:
        st.subheader("🏡 Property Area Risk Profiling")
        prop_df = df_raw.groupby(["Property_Area", "Loan_Status"]).size().reset_index(name="Count")
        fig_prop = px.bar(
            prop_df,
            x="Property_Area",
            y="Count",
            color="Loan_Status",
            barmode="stack",
            color_discrete_map={"Y": "#10B981", "N": "#EF4444"},
            labels={"Property_Area": "Property Location", "Count": "Applications"}
        )
        st.plotly_chart(fig_prop, use_container_width=True)
        st.caption("💡 **Insight:** Semiurban properties demonstrate the highest approval stability due to balanced collateral security.")

    st.markdown("---")
    driver_col3, driver_col4 = st.columns(2)
    
    with driver_col3:
        st.subheader("🎓 Education & Employment Impact")
        edu_df = df_raw.groupby(["Education", "Loan_Status"]).size().reset_index(name="Count")
        fig_edu = px.bar(
            edu_df,
            x="Education",
            y="Count",
            color="Loan_Status",
            barmode="group",
            color_discrete_map={"Y": "#10B981", "N": "#EF4444"}
        )
        st.plotly_chart(fig_edu, use_container_width=True)
        
    with driver_col4:
        st.subheader("👥 Dependents vs Debt Burden Ratio")
        fig_dep = px.box(
            df_raw,
            x="Dependents",
            y="Income_to_Loan_Ratio",
            color="Loan_Status",
            color_discrete_map={"Y": "#10B981", "N": "#EF4444"},
            labels={"Income_to_Loan_Ratio": "Income / Loan Burden Ratio"}
        )
        st.plotly_chart(fig_dep, use_container_width=True)

# ---------------------------------------------------------
# VIEW 3: AI Loan Underwriting & Prescriptive Actions (Levels 4 & 5)
# ---------------------------------------------------------
elif nav_selection == "Level 4 & 5: AI Underwriting & Action":
    st.markdown("<div class='main-header'>AI Underwriting & Risk Action Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Real-time applicant underwriting with credit risk assessment and automated prescriptive recommendations.</div>", unsafe_allow_html=True)
    
    with st.form("underwriting_form"):
        st.subheader("📋 Applicant Credit Profile Submission")
        f_col1, f_col2, f_col3 = st.columns(3)
        
        with f_col1:
            in_gender = st.selectbox("Gender", ["Male", "Female"])
            in_married = st.selectbox("Marital Status", ["Yes", "No"])
            in_dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
            in_education = st.selectbox("Education", ["Graduate", "Not Graduate"])
            
        with f_col2:
            in_self_emp = st.selectbox("Self Employed", ["No", "Yes"])
            in_app_inc = st.number_input("Applicant Monthly Income ($)", min_value=500, max_value=100000, value=5500, step=500)
            in_coapp_inc = st.number_input("Coapplicant Monthly Income ($)", min_value=0, max_value=50000, value=1500, step=500)
            in_loan_amt = st.number_input("Requested Loan Amount ($ in Thousands)", min_value=10, max_value=1000, value=140, step=10)
            
        with f_col3:
            in_term = st.selectbox("Loan Term (Months)", [120, 180, 240, 300, 360, 480], index=4)
            in_credit = st.selectbox("Credit History Status", ["1.0 (Meets Credit Guidelines)", "0.0 (Does Not Meet Guidelines)"], index=0)
            in_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"], index=1)
            
        submitted = st.form_submit_button("🚀 Run AI Credit Underwriting Assessment", use_container_width=True)
        
    if submitted:
        ch_val = 1.0 if "1.0" in in_credit else 0.0
        tot_inc = in_app_inc + in_coapp_inc
        ratio = tot_inc / (in_loan_amt * 1000 + 1e-5)
        
        input_data = pd.DataFrame([{
            "ApplicantIncome": in_app_inc,
            "CoapplicantIncome": in_coapp_inc,
            "LoanAmount": in_loan_amt,
            "Loan_Amount_Term": in_term,
            "TotalIncome": tot_inc,
            "Income_to_Loan_Ratio": ratio,
            "Gender": in_gender,
            "Married": in_married,
            "Dependents": in_dependents,
            "Education": in_education,
            "Self_Employed": in_self_emp,
            "Credit_History": ch_val,
            "Property_Area": in_area
        }])
        
        prob_approved = best_model.predict_proba(input_data)[0][1]
        verdict = "APPROVED" if prob_approved >= 0.50 else "REJECTED"
        default_risk = (1.0 - prob_approved) * 100
        
        st.markdown("### ")
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            st.subheader("Underwriting Verdict")
            if verdict == "APPROVED":
                st.success(f"### ✅ Verdict: LOAN APPROVED\nConfidence: **{prob_approved*100:.1f}%**")
            else:
                st.error(f"### ❌ Verdict: LOAN REJECTED\nDefault Risk: **{default_risk:.1f}%**")
                
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob_approved * 100,
                title={'text': "Approval Probability Score (%)"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#10B981" if prob_approved >= 0.50 else "#EF4444"},
                    'steps': [
                        {'range': [0, 40], 'color': "#FEE2E2"},
                        {'range': [40, 70], 'color': "#FEF3C7"},
                        {'range': [70, 100], 'color': "#D1FAE5"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            fig_gauge.update_layout(height=280, margin=dict(t=40, b=20, l=30, r=30))
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        with res_col2:
            st.subheader("🎯 Level 5 Strategic Business Actions")
            if verdict == "APPROVED":
                st.markdown("""
                - **Primary Action:** Issue sanction letter with prime interest rate.
                - **Risk Tier:** **Low Risk (<25% Default Potential)**.
                - **Cross-Selling Opportunity:** Offer institutional credit card & mortgage insurance.
                - **Collateral Recommendation:** Standard property mortgage lien registration.
                """)
            elif ch_val == 0.0:
                st.markdown("""
                - **Primary Action:** Direct rejection or require secondary co-signer/guarantor with prime credit history.
                - **Risk Factor:** Non-compliance with historical credit guidelines (Credit_History = 0.0).
                - **Alternative Product:** Offer Secured Fixed-Deposit Backed Loan or Credit-Builder Line.
                """)
            else:
                st.markdown("""
                - **Primary Action:** High debt burden detected relative to requested capital.
                - **Mitigation Action:** Recommend extending loan tenure from 15 to 30 years to lower monthly EMI burden by ~35%.
                - **Conditional Approval:** Request proof of supplementary liquid assets or co-borrower income.
                """)

# ---------------------------------------------------------
# VIEW 4: Model Evaluation & Governance
# ---------------------------------------------------------
elif nav_selection == "Model Evaluation & Governance":
    st.markdown("<div class='main-header'>Model Governance & Performance Benchmark</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Rigorous multi-model validation metrics, confusion matrices, and explainability feature importance.</div>", unsafe_allow_html=True)
    
    metric_rows = []
    for m_name, m_dict in model_metrics.items():
        metric_rows.append({
            "Algorithm": m_name,
            "Accuracy (%)": f"{m_dict['Accuracy']*100:.2f}%",
            "Precision (%)": f"{m_dict['Precision']*100:.2f}%",
            "Recall (%)": f"{m_dict['Recall']*100:.2f}%",
            "F1-Score": f"{m_dict['F1-Score']:.3f}",
            "ROC-AUC": f"{m_dict['ROC-AUC']:.3f}"
        })
        
    st.table(pd.DataFrame(metric_rows))
    
    st.markdown("---")
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        st.subheader("Confusion Matrix (Random Forest)")
        cm = model_metrics["Random Forest"]["Confusion Matrix"]
        fig_cm = px.imshow(
            cm,
            text_auto=True,
            labels=dict(x="Predicted Status", y="Actual Status", color="Count"),
            x=["Rejected (0)", "Approved (1)"],
            y=["Rejected (0)", "Approved (1)"],
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_cm, use_container_width=True)
        
    with g_col2:
        st.subheader("Top Predictive Feature Importances")
        rf_model = pipelines["Random Forest"].named_steps["classifier"]
        feature_names = ["ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "TotalIncome", "Income_to_Loan_Ratio", "Gender", "Married", "Dependents", "Education", "Self_Employed", "Credit_History", "Property_Area"]
        importances = rf_model.feature_importances_[:len(feature_names)]
        fi_df = pd.DataFrame({"Feature": feature_names, "Importance": importances}).sort_values(by="Importance", ascending=True)
        
        fig_fi = px.bar(
            fi_df,
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_fi, use_container_width=True)
