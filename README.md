# What's the rate?
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

  
