# What's the rate?
*VISIT* https://whatstherate.streamlit.app/ 
## OBJECTIVES:
- To be able to predict the ever-changing EUR-GBP exchange rate with:
  **AT LEAST** 65% directional accuracy- very important
  **AT MOST** Mean Absolute Percentage Error of 0.35% (fingers crossed)
- To provide statistical analysis, i.e percentiles, rankings
- To show probability distributions
- To compare current rates to historical averages
## Repo ##
notebooks/: This directory houses the primary analytical workflow. It works via:
- 1. data exploration (02_exploratory_analysis)
- 2. the creation of technical indicators (03_feature_engineering)
- 3. covering model training with a tree-based ensemble algorithm (04_model_development)
- 4. including thorough performance and error assessment (05_model_evaluation)
- 5. the logic for generating actionable trading insights (06_insights_generation).

scripts/download_data.py: A Python script designed to automatically fetch historical currency pair data using the Yahoo Finance API.

data/: Structured into two subdirectories: /raw for preserving original data downloads and /processed for the cleaned, augmented datasets that serve as input for the modeling phase.

models/: A storage location for the serialized model artifact (.pkl) and associated feature configuration files, enabling the trained logic to be deployed in external applications.

visual_assets/: Contains a set of PNG visualizations—including historical_trend.png, prediction_results.png, and feature_importance.png—that graphically represent model outcomes and underlying data patterns.

<ins> The system successfully navigated deployment environment constraints and achieved a test set Mean Absolute Error (MAE) of 0.00299. </ins>

## Live Application: WhatsTheRate
The project is deployed as a multi-page interactive web application using Streamlit. It provides a user-friendly interface for non-technical users to interpret complex market data and AI forecasts.

Core Features:
 * Market Dashboard: Real-time visualization of the EUR/GBP rate vs. its 30-day moving average.
* AI Price Projections: Next-session forecasts powered by a Random Forest Regressor.
* Reliability Rating: A custom-built Confidence Score that uses the variance between decision trees to quantify how "sure" the model is about its prediction.
* Optimal Transfer Strategy: Statistical analysis of historical data to identify the best days of the week for currency exchange.

## Automated Data Pipeline (DevOps)
This project is fully autonomous. It does not require manual data updates or retraining.

* GitHub Actions: A CI/CD workflow runs every night at midnight (UTC).
* Auto-Update: The system fetches the latest market data from the Yahoo Finance API, performs feature engineering, and retrains the model.
* Auto-Push: Updated data and model artifacts are automatically committed back to the repository, ensuring the Streamlit app always displays fresh insights.

## Tech Stack
* Language: **Python 3.10**
* Machine Learning: **Scikit-Learn** (Random Forest Regressor)
* Data Handling: **Pandas, NumPy, yfinance**
* Frontend: **Streamlit**
* DevOps: **GitHub Actions (YAML)**
* Environment: **Virtualenv / Pip**

**Feature Engineering**
To move beyond simple price tracking, the AI model uses several technical indicators to capture market momentum:

* MA-30: 30-day Moving Average to identify long-term trends.
* Daily Returns: Calculated percentage change to capture price momentum.
* Volatility: 5-day rolling standard deviation to assess market "fear."
* Lagged Rates: Yesterday's closing price to provide immediate context for the model.

## License Notice
This is **proprietary software** owned by sha2w2.

You may **view** this code for learning purposes only.

X No commercial use
X No modifications
X No derivatives
X No use without permission

See the [LICENSE](LICENSE) file for complete terms.

For any use beyond viewing, please contact sha2w2.
  
