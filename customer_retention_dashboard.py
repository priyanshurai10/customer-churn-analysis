import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, roc_auc_score

# Page setup
st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

st.title("Customer Churn Analysis Dashboard")
st.write("This dashboard helps us understand why customers leave and predicting basic risk.")

# --- 1. DATA CLEANING & LOADING ---
@st.cache_data
def load_and_clean_data():
    # URL to the raw dataset on GitHub
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    
    # Load dataset
    df = pd.read_csv(url)
    
    # Check for missing values in TotalCharges
    # TotalCharges is initially a string, some values are just spaces " "
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # Drop missing values (there are usually just 11 in this dataset)
    df = df.dropna(subset=['TotalCharges'])
    
    # Create a ChurnFlag (1 for Yes, 0 for No)
    df['ChurnFlag'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    # Create simple tenure groups
    def group_tenure(t):
        if t <= 12: return "0-1 Year"
        elif t <= 24: return "1-2 Years"
        elif t <= 48: return "2-4 Years"
        else: return "4+ Years"
        
    df['TenureGroup'] = df['tenure'].apply(group_tenure)
    
    return df

df = load_and_clean_data()

# --- 2. KPI SECTION ---
st.header("1. Business KPIs")

total_customers = len(df)
churn_rate = df['ChurnFlag'].mean() * 100
total_monthly_revenue = df['MonthlyCharges'].sum()
avg_monthly_charge = df['MonthlyCharges'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churn Rate", f"{churn_rate:.1f}%")
col3.metric("Total Monthly Charges", f"${total_monthly_revenue:,.0f}")
col4.metric("Avg Monthly Charge", f"${avg_monthly_charge:.2f}")

st.divider()

# --- 3. DATA ANALYSIS (CHARTS) ---
st.header("2. Data Analysis")
st.write("Looking at how churn is affected by different factors.")

row1_col1, row1_col2, row1_col3 = st.columns(3)

# Churn by Contract
with row1_col1:
    st.subheader("Churn by Contract")
    contract_churn = df.groupby('Contract')['ChurnFlag'].mean() * 100
    fig1, ax1 = plt.subplots(figsize=(5,3))
    contract_churn.plot(kind='bar', color='skyblue', ax=ax1)
    ax1.set_ylabel("Churn Rate (%)")
    ax1.set_xlabel("")
    plt.xticks(rotation=0)
    st.pyplot(fig1)

# Churn by Internet Service
with row1_col2:
    st.subheader("Churn by Internet Service")
    internet_churn = df.groupby('InternetService')['ChurnFlag'].mean() * 100
    fig2, ax2 = plt.subplots(figsize=(5,3))
    internet_churn.plot(kind='bar', color='salmon', ax=ax2)
    ax2.set_ylabel("Churn Rate (%)")
    ax2.set_xlabel("")
    plt.xticks(rotation=0)
    st.pyplot(fig2)

# Churn by Tenure Group
with row1_col3:
    st.subheader("Churn by Tenure")
    tenure_churn = df.groupby('TenureGroup')['ChurnFlag'].mean() * 100
    # sorting groups logically
    tenure_churn = tenure_churn.reindex(["0-1 Year", "1-2 Years", "2-4 Years", "4+ Years"])
    fig3, ax3 = plt.subplots(figsize=(5,3))
    tenure_churn.plot(kind='bar', color='lightgreen', ax=ax3)
    ax3.set_ylabel("Churn Rate (%)")
    ax3.set_xlabel("")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

st.divider()

# --- 4. CUSTOMER/RISK ANALYSIS TABLE ---
st.header("3. Risk Segment Analysis")
st.write("Table showing customer segments and their churn risk.")

# Grouping by contract and internet service
segment_analysis = df.groupby(['Contract', 'InternetService']).agg(
    Number_of_Customers=('customerID', 'count'),
    Churn_Rate=('ChurnFlag', lambda x: x.mean() * 100),
    Avg_Monthly_Charge=('MonthlyCharges', 'mean')
).reset_index()

# Formatting columns for better display
segment_analysis['Churn_Rate'] = segment_analysis['Churn_Rate'].round(1).astype(str) + '%'
segment_analysis['Avg_Monthly_Charge'] = '$' + segment_analysis['Avg_Monthly_Charge'].round(2).astype(str)

st.dataframe(segment_analysis, use_container_width=True)

st.divider()

# --- 5. BASIC MACHINE LEARNING ---
st.header("4. Basic Machine Learning Model")
st.write("I built a simple Logistic Regression model to find patterns and predict churn risk.")

@st.cache_resource
def train_model(data):
    # Select features for the simple model
    features = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Contract', 'InternetService', 'PaperlessBilling']
    X = data[features].copy()
    y = data['ChurnFlag']
    
    # Categorical encoding using get_dummies
    X = pd.get_dummies(X, drop_first=True)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scaling numerical features
    scaler = StandardScaler()
    X_train[['tenure', 'MonthlyCharges', 'TotalCharges']] = scaler.fit_transform(X_train[['tenure', 'MonthlyCharges', 'TotalCharges']])
    X_test[['tenure', 'MonthlyCharges', 'TotalCharges']] = scaler.transform(X_test[['tenure', 'MonthlyCharges', 'TotalCharges']])
    
    # Train Logistic Regression
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    return f1, roc_auc, model

f1, roc_auc, model = train_model(df)

col_m1, col_m2 = st.columns(2)
col_m1.metric("Model F1 Score", f"{f1:.2f}")
col_m2.metric("Model ROC-AUC", f"{roc_auc:.2f}")

st.info("Note: This model is a basic baseline. It does not guarantee exactly who will leave, but it helps us identify risk patterns better than guessing.")

st.divider()

# --- 6. BUSINESS INSIGHTS ---
st.header("5. Business Insights")

st.markdown("### ⚠️ Risk")
st.write("Customers with Month-to-Month contracts and Fiber Optic internet have the highest churn rate. Also, most people who leave tend to leave in their first year (0-1 Year tenure group).")

st.markdown("### 💡 Opportunity")
st.write("Customers on 1-Year or 2-Year contracts are very loyal. If we can convince new customers to take longer contracts, they are more likely to stay.")

st.markdown("### 🛠️ Possible Action")
st.markdown("""
- **Better Onboarding:** Focus heavily on the first 6-12 months of a customer's journey.
- **Targeted Retention Offers:** Give a discount to Month-to-Month customers if they upgrade to a 1-year contract.
- **Check Fiber Optic issues:** Since Fiber Optic customers are leaving often, we should check if our Fiber service has technical problems or if it is priced too high compared to competitors.
""")

st.divider()

# --- 7. CUSTOMER EXPLORER ---
st.header("6. Customer Explorer")
st.write("Use the filters below to view specific customer groups.")

filt_col1, filt_col2 = st.columns(2)
with filt_col1:
    contract_filter = st.selectbox("Select Contract Type", df['Contract'].unique())
with filt_col2:
    internet_filter = st.selectbox("Select Internet Service", df['InternetService'].unique())

# Filtering the dataframe
filtered_df = df[(df['Contract'] == contract_filter) & (df['InternetService'] == internet_filter)]

# Showing a few useful columns
display_cols = ['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges', 'Churn']
st.write(f"Showing customers with **{contract_filter}** contract and **{internet_filter}** internet:")
st.dataframe(filtered_df[display_cols].head(100)) # show max 100 for clean UI
