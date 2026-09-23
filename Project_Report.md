# Project Report: Customer Churn Analysis

## 1. Introduction
Hi, this is my data analytics project submitted for the IBM SkillsBuild Data Analytics with AI internship. In this project, I used Python to analyze customer churn.

## 2. Problem Statement
The business problem is that customers are leaving the service. I wanted to find out why they are leaving and what the company can do to retain them.

## 3. Objective
My main objective was to answer simple business questions:
- How many customers are there?
- What percentage of customers have churned?
- Which customer groups have higher churn?
- Does contract type or internet service affect churn?
- What possible business action can be taken?

## 4. Dataset
I used the IBM Telco Customer Churn sample dataset. It contains customer demographics, account information (like contract type and monthly charges), and whether the customer churned.

## 5. Data Cleaning
I used Pandas for data cleaning:
- Loaded the CSV data.
- Checked for missing values.
- Converted the 'TotalCharges' column from text to numeric format.
- Dropped a few rows where 'TotalCharges' was missing.
- Created a numeric 'ChurnFlag' column (1 or 0).
- Created a tenure group column to make the charts easier to read.

## 6. Exploratory Data Analysis
I created simple charts using Matplotlib to see the patterns in the data visually. I focused on comparing the churn rate against different columns like contract type and internet service.

## 7. KPIs
Based on the clean dataset:
- Total Customers: 7,032
- Churn Rate: Around 26.6%
- Average Monthly Charges: Around $64.80

## 8. Churn Analysis
From the charts, I observed that:
- Customers on month-to-month contracts churn the most.
- Customers with Fiber Optic internet have a higher churn rate compared to DSL users.
- New customers (0-1 year) have the highest churn rate.

## 9. Customer Segmentation
I grouped the customers into simple segments based on their contract and internet choices to understand where the biggest risks are.

## 10. Risk Identification
**Observation:** Month-to-Month contract customers have a churn rate of around 42%.
**Possible Risk:** These customers feel no commitment and can leave at any time. The Fiber Optic customers also show high churn, which could suggest a technical or pricing problem.

## 11. Opportunities
Customers on 1-Year or 2-Year contracts are very loyal, with churn rates below 10%. This is a strong opportunity area.

## 12. Possible Actions
- **Better Onboarding:** Provide more support during a customer's first year.
- **Targeted Retention Offers:** Offer a discount to month-to-month customers if they switch to a 1-year contract.
- **Check Fiber Optic Service:** The company should check if their Fiber Optic service has technical issues causing people to leave.

## 13. Prediction Model
I built a basic Logistic Regression model using Scikit-Learn. I used train_test_split to divide the data, converted text to numbers using get_dummies, and scaled the numeric columns. This model predicts the likelihood of churn based on customer features.

## 14. Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Streamlit

## 15. Results/Findings
The dataset helped me confirm that contract type and internet service strongly relate to churn. The basic Logistic Regression model achieved an ROC-AUC score of 0.84 and an F1 score of 0.59, showing it can find basic risk patterns.

## 16. Limitations
This is a simple student project. The prediction model is a basic baseline and does not guarantee exactly which customer will leave. It is just a helpful tool for risk identification.

## 17. Conclusion
This project successfully moved from raw data to data cleaning, analysis, and finally to business insights. It helped me learn how data can guide basic business actions.

## 18. Project Files
- PriyanshuRai_CustomerChurnAnalysis.py: The main Streamlit dashboard.
- requirements.txt: The required libraries.
- README.md: Project overview.
- PriyanshuRai_ProjectReport.docx: This report.