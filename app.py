import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, roc_auc_score

# ==================================================
# A. Project Title & Setup
# ==================================================
st.set_page_config(page_title="Customer Churn Analysis", layout="wide")
st.title("Customer Churn Analysis")

# ==================================================
# B. Short Introduction
# ==================================================
st.write("""
Hi! This is a simple student project for my Data Analytics internship. 
It analyzes telecom customer data to understand why customers leave (churn). 
The goal is to find patterns in the data, identify groups with high churn risk, and suggest basic business actions.
""")
st.divider()

# ==================================================
# Data Cleaning & Loading
# ==================================================
@st.cache_data
def load_and_clean_data():
    # Load dataset from the raw GitHub link
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    df = pd.read_csv(url)
    
    # Check for missing values in TotalCharges (stored as blank spaces)
    # Convert text to numeric, 'coerce' turns blank spaces into NaN
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # Remove rows with missing TotalCharges (very few rows)
    df = df.dropna(subset=['TotalCharges'])
    
    # Create a simple numeric ChurnFlag (1 for churned, 0 for stayed)
    df['ChurnFlag'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    # Create simple tenure groups to make analysis easier
    def group_tenure(t):
        if t <= 12: return "0-1 Year"
        elif t <= 24: return "1-2 Years"
        elif t <= 48: return "2-4 Years"
        else: return "4+ Years"
        
    df['TenureGroup'] = df['tenure'].apply(group_tenure)
    
    return df

df = load_and_clean_data()

# ==================================================
# C. Dataset Information
# ==================================================
st.header("1. Dataset Information")
st.write("This project uses the IBM Telco Customer Churn sample dataset.")
st.write(f"- **Number of customers in data:** {len(df)}")
st.write("- **Important columns used:** Contract, InternetService, tenure, MonthlyCharges, TotalCharges")
st.write("- **Churn column:** Represents whether the customer left ('Yes') or stayed ('No').")
st.divider()

# ==================================================
# D. KPI Section
# ==================================================
st.header("2. Key Performance Indicators (KPIs)")

total_customers = len(df)
churn_rate = (df['ChurnFlag'].sum() / total_customers) * 100
avg_monthly_charges = df['MonthlyCharges'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Overall Churn Rate", f"{churn_rate:.1f}%")
col3.metric("Average Monthly Charges", f"${avg_monthly_charges:.2f}")

st.divider()

# ==================================================
# 8. Analysis (Charts)
# ==================================================
st.header("3. Data Analysis")
st.write("I created simple charts to see which customer groups have higher churn.")

c1, c2, c3 = st.columns(3)

# 1. Churn by Contract
with c1:
    st.subheader("Churn by Contract")
    contract_churn = df.groupby('Contract')['ChurnFlag'].mean() * 100
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    contract_churn.plot(kind='bar', color='skyblue', ax=ax1)
    ax1.set_ylabel("Churn Rate (%)")
    ax1.set_title("Month-to-Month contracts have highest churn")
    plt.xticks(rotation=0)
    st.pyplot(fig1)

# 2. Churn by Internet Service
with c2:
    st.subheader("Churn by Internet Service")
    internet_churn = df.groupby('InternetService')['ChurnFlag'].mean() * 100
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    internet_churn.plot(kind='bar', color='lightcoral', ax=ax2)
    ax2.set_ylabel("Churn Rate (%)")
    ax2.set_title("Fiber optic users churn more")
    plt.xticks(rotation=0)
    st.pyplot(fig2)

# 3. Churn by Tenure
with c3:
    st.subheader("Churn by Tenure")
    tenure_churn = df.groupby('TenureGroup')['ChurnFlag'].mean() * 100
    tenure_churn = tenure_churn.reindex(["0-1 Year", "1-2 Years", "2-4 Years", "4+ Years"])
    fig3, ax3 = plt.subplots(figsize=(4, 3))
    tenure_churn.plot(kind='bar', color='lightgreen', ax=ax3)
    ax3.set_ylabel("Churn Rate (%)")
    ax3.set_title("New customers (0-1 Year) leave the most")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

st.divider()

# ==================================================
# 9 & 10. Business Insights & Risk/Opportunity Table
# ==================================================
st.header("4. Business Insights & Segments")
st.write("Based on the charts, here is a simple breakdown of risks, opportunities, and possible actions.")

insights_data = {
    "Segment": ["Month-to-Month Contract", "Fiber Optic Internet", "1-Year & 2-Year Contract", "Tenure (0-1 Year)"],
    "Observation": [
        "Highest churn rate (around 42%).",
        "Churn rate is noticeably higher than DSL.",
        "Very low churn rate (less than 10%).",
        "Most churn happens in the first 12 months."
    ],
    "Possible Risk": [
        "Customers feel no commitment and leave easily.",
        "Could indicate a technical problem or high price.",
        "No major risk, highly stable.",
        "Poor initial onboarding or early dissatisfaction."
    ],
    "Possible Action": [
        "Offer targeted retention discounts to upgrade to a 1-year contract.",
        "Check technical support tickets for Fiber Optic customers.",
        "Focus marketing on selling these long-term contracts.",
        "Provide better customer support in the first year."
    ]
}
st.table(pd.DataFrame(insights_data))

st.divider()

# ==================================================
# 12. Prediction Model
# ==================================================
st.header("5. Basic Prediction Model")
st.write("""
This model is a basic example of predicting whether a customer may churn based on available customer information. 
It uses Logistic Regression.
""")

@st.cache_resource
def run_model(data):
    # Select basic columns
    features = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Contract', 'InternetService']
    X = data[features].copy()
    y = data['ChurnFlag']
    
    # Convert text columns into numbers
    X = pd.get_dummies(X, drop_first=True)
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale numeric columns
    scaler = StandardScaler()
    numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])
    
    # Train Logistic Regression
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    
    # Test model
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate simple metrics
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    return f1, roc_auc

f1, roc_auc = run_model(df)

m1, m2 = st.columns(2)
m1.metric("Calculated F1 Score", f"{f1:.2f}")
m2.metric("Calculated ROC-AUC", f"{roc_auc:.2f}")
st.caption("Note: This is not a production-ready model. It simply shows that the algorithm can find basic risk patterns better than random guessing.")

st.divider()

# ==================================================
# 11. Customer Explorer
# ==================================================
st.header("6. Customer Explorer")
st.write("Use the dropdowns to filter and view matching customer records.")

e1, e2 = st.columns(2)
with e1:
    filter_contract = st.selectbox("Contract Type", df['Contract'].unique())
with e2:
    filter_internet = st.selectbox("Internet Service", df['InternetService'].unique())

filtered_data = df[(df['Contract'] == filter_contract) & (df['InternetService'] == filter_internet)]
st.write(f"Showing customers with **{filter_contract}** and **{filter_internet}**:")
st.dataframe(filtered_data[['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges', 'Churn']].head(50))
