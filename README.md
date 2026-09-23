# Customer Churn Analysis

## About the Project
Hi, I created this project as part of my IBM SkillsBuild Data Analytics with AI internship. It is a simple data analytics project built with Python and Streamlit.

## Objective
I wanted to analyze customer data to understand:
- How many customers are leaving.
- Which customer groups have higher churn.
- Whether contract type or internet service affects churn.
- What possible business actions can be taken to reduce this churn.

## Dataset
I used the IBM Telco Customer Churn sample dataset.
**Dataset Source:** [Telco-Customer-Churn.csv](https://github.com/IBM/telco-customer-churn-on-icp4d/blob/master/data/Telco-Customer-Churn.csv)

*(Note: I checked this against the IBM masterclass requirement. The masterclasses primarily used e-commerce data, so this Telecom dataset is safe to use for the final project without conflict).*

## What I Analyzed
I explored the data to understand the relationship between churn and:
- Contract type (Month-to-month vs 1-Year/2-Year)
- Internet service (DSL vs Fiber Optic)
- Tenure (How long they have been a customer)
- Monthly charges

## Tools Used
- Python
- Pandas (for data cleaning)
- NumPy (for numeric operations)
- Matplotlib (for simple charts)
- Scikit-learn (for basic prediction)
- Streamlit (for building the simple dashboard)

## Main Project Flow
Data → Cleaning → Analysis → Insights → Risk → Opportunity → Possible Action

## Prediction
I included a basic Logistic Regression model. It is trained on the customer data to predict if someone is likely to churn. I calculated the F1 score and ROC-AUC score.

## How to Run
To run this project locally, use your terminal and type:

1. Install the required libraries:
```bash
pip install -r requirements.txt
```

2. Run the main application file:
```bash
streamlit run app.py
```

## Project Files
- `app.py`: The main Python application file containing the data cleaning, charts, and dashboard UI.
- `requirements.txt`: The list of Python libraries needed to run the code.
- `README.md`: This overview file.
- `Project_Report.md`: The text version of my project report.
- `project_report.docx`: The Microsoft Word version of my project report.

## Limitations
This is a student project. The prediction model is a basic baseline example and is not a production-ready system. It simply helps to show patterns in the data.
