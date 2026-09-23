import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# loading some dummy data so the app runs without uploading a csv every time
@st.cache_data
def get_data():
    np.random.seed(42)
    # creating 500 fake customers
    data = pd.DataFrame({
        'tenure_months': np.random.randint(1, 72, 500),
        'monthly_charges': np.random.randint(20, 120, 500),
        'support_tickets': np.random.randint(0, 5, 500),
        'age': np.random.randint(18, 70, 500)
    })
    
    # rule for churn: high tickets and low tenure means they probably leave
    risk_score = (data['support_tickets'] * 20) - (data['tenure_months'] * 0.5)
    data['churn'] = (risk_score > 30).astype(int)
    return data

df = get_data()

# training a simple model
X = df.drop('churn', axis=1)
y = df['churn']
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

rf_model = RandomForestClassifier(random_state=10)
rf_model.fit(x_train, y_train)

# Start of the Streamlit App
st.title("Customer Churn Analysis & Prediction")
st.write("This dashboard helps us find out which customers are likely to leave our service and why.")

# Section 1: Dashboard KPIs
st.header("1. Business KPIs")
st.write("Here is the summary of our customer data:")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(df))
col2.metric("Overall Churn Rate", f"{(df['churn'].mean() * 100):.1f}%")
col3.metric("Avg Monthly Charges", f"${df['monthly_charges'].mean():.2f}")

# Section 2: Data Visualizations
st.header("2. Data Analysis")
st.write("Let's look at what causes customers to churn.")

fig, ax = plt.subplots()
# grouping by support tickets to see churn rate
churn_by_tickets = df.groupby('support_tickets')['churn'].mean() * 100
churn_by_tickets.plot(kind='bar', color='orange', ax=ax)
ax.set_ylabel('Churn Rate %')
ax.set_xlabel('Number of Support Tickets')
ax.set_title('Churn Rate vs Support Tickets')
st.pyplot(fig)
st.write("Observation: Customers who open more support tickets have a much higher chance of leaving. We need to improve our customer service.")

st.divider()

# Section 3: Prediction
st.header("3. Predict Churn for a Customer")
st.write("Enter customer details below to check if they are at risk of churning.")

t_months = st.number_input("Tenure (Months)", 1, 100, 12)
m_charges = st.number_input("Monthly Charges ($)", 10, 200, 50)
s_tickets = st.number_input("Support Tickets Opened", 0, 10, 1)
c_age = st.number_input("Customer Age", 18, 100, 30)

if st.button("Check Risk"):
    # make a prediction
    input_data = pd.DataFrame([[t_months, m_charges, s_tickets, c_age]], 
                              columns=['tenure_months', 'monthly_charges', 'support_tickets', 'age'])
    
    pred = rf_model.predict(input_data)[0]
    
    if pred == 1:
        st.error("Action Required: High risk of churn! We should offer them a discount or call them.")
    else:
        st.success("Safe: This customer looks happy and is likely to stay.")
