# Customer Churn Analysis

Hi, I am a B.Tech CSE student and this is my student project for the IBM SkillsBuild / BharatCares Data Analytics internship.

## About the project
I made this project to understand customer churn data. Churn means when a customer leaves a company. Finding out why people leave helps a business take action and save money.

## Problem statement
The main questions I wanted to answer are:
- How many customers are leaving?
- Which customer groups have higher churn?
- Does contract type or internet service affect churn?
- What possible business actions can be taken to reduce this?

## Dataset
I used the IBM Telco Customer Churn sample dataset. It contains data about a telecom company's customers, their services, how much they pay, and whether they churned (left) or not.
Dataset source: [IBM Telco Customer Churn dataset](https://github.com/IBM/telco-customer-churn-on-icp4d/blob/master/data/Telco-Customer-Churn.csv)

## What I did

### 1. Data Cleaning
- Loaded the dataset using Pandas.
- Converted the `TotalCharges` column to numeric because it was stored as text.
- Removed rows with missing values (there were very few).
- Created a `ChurnFlag` (1/0) for easy calculations.
- Grouped `tenure` into simple groups like "0-1 Year", "1-2 Years".

### 2. Analysis
I created simple charts using Matplotlib to see patterns. I found that Month-to-Month contracts have very high churn. Also, people with Fiber Optic internet tend to leave more.

### 3. Machine Learning
I trained a basic Logistic Regression model using `scikit-learn` to predict churn risk. I used one-hot encoding for categorical text data and scaled the numerical data. 
*Note: This prediction model is only a basic baseline. It doesn't guarantee exactly who will leave, but it helps find risk patterns better than guessing.*

### 4. Business Insights
I added a section in the dashboard explaining the Risks, Opportunities, and Possible Actions the business can take (like offering discounts to switch to 1-year contracts).

## Technologies used
- Python
- Pandas & NumPy (for data handling)
- Matplotlib (for simple charts)
- Scikit-Learn (for basic machine learning)
- Streamlit (for building the web dashboard)

## How to run the project

1. Open your terminal or command prompt.
2. Install the required libraries by typing:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit dashboard by typing:
   ```bash
   streamlit run customer_retention_dashboard.py
   ```
4. The dashboard will automatically open in your web browser.

## Project files
- `customer_retention_dashboard.py`: The main python code that cleans data, trains the model, and shows the UI.
- `requirements.txt`: The list of libraries needed.
- `README.md`: This file explaining the project.
- `project_report.md` / `project_report.docx`: The text report summarizing my work.
