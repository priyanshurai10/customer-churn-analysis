# Project Report: Customer Churn Analysis

## 1. Introduction
Hi, I am a B.Tech CSE student. This is my data analytics project created as part of the IBM SkillsBuild / BharatCares internship. The project focuses on Customer Churn Analysis, which means studying the data of customers who stop doing business with a company.

## 2. Problem Statement
The main goal of this project is to analyze customer data to understand:
- How many customers are leaving.
- Which customer groups have a higher churn rate.
- Whether factors like contract type, internet service, and customer tenure affect churn.
- What possible business actions the company can take to retain customers.

## 3. Dataset
I used the IBM Telco Customer Churn sample dataset. It includes information about telecom customers, such as their tenure, monthly charges, contract type, internet service, and whether they left the company (churned).

## 4. Data Cleaning
Before analyzing the data, I cleaned it using Pandas in Python. I:
- Loaded the dataset from the CSV link.
- Converted the 'TotalCharges' column into a numeric format (it had some empty spaces).
- Removed a few rows that had missing values in TotalCharges.
- Created a simple 'ChurnFlag' column (1 for Yes, 0 for No) to make calculations easier.
- Created tenure groups like '0-1 Year' to make the charts simpler to read.

## 5. Analysis
I used Matplotlib to create simple charts and found some clear patterns:
- Churn by Contract: Customers on a 'Month-to-Month' contract have a much higher churn rate compared to those on 1-year or 2-year contracts.
- Churn by Internet Service: Customers using 'Fiber optic' internet leave more often than those using DSL or no internet.
- Churn by Tenure: Most churn happens in the first year (0-1 Year group).

## 6. Machine Learning Model
I built a basic Logistic Regression model using Scikit-Learn to see if I could predict churn. I split the data into training (80%) and testing (20%) sets. I converted text columns into numbers using one-hot encoding and scaled the numerical columns so the model could learn better.

## 7. Results
When I tested the model on the test data, it gave an ROC-AUC score of around 0.84 and an F1 score of around 0.59. This means the model is decent at recognizing risk patterns, but it is just a basic baseline and does not guarantee exactly who will leave.

## 8. Risk, Opportunity, and Possible Action
**Risk:**
Customers with Month-to-Month contracts and Fiber Optic internet are at high risk of leaving.

**Opportunity:**
Customers on 1-Year or 2-Year contracts are very loyal. The company should focus on getting more people into these contracts.

**Possible Action:**
- Better Onboarding: Give more support during the first 6-12 months.
- Targeted Retention Offers: Offer a small discount to month-to-month customers if they switch to a 1-year contract.
- Check the Fiber Optic service to see if there are technical issues causing people to leave.

## 9. Technologies Used
- Python
- Pandas & NumPy (Data Cleaning and Handling)
- Matplotlib (Data Visualization)
- Scikit-Learn (Basic Machine Learning)
- Streamlit (Dashboard UI)

## 10. Conclusion
In conclusion, this project helped me learn how to take raw data, clean it, find useful patterns, and suggest basic business actions. It was a great learning experience for practical data analytics.