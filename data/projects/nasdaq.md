# NASDAQ-100 Market Prediction using Machine Learning

## Project Summary

Developed a machine learning system to predict NASDAQ-100 market behaviour using historical stock prices from the top 20 NASDAQ constituent companies combined with macroeconomic indicators.

The project included two predictive models:

1. Classification model to predict market direction (Bullish or Bearish)
2. Regression model to predict next-day returns

The solution was developed using Python and XGBoost following the CRISP-DM methodology.

## Business Problem

Investors often struggle to determine future market behaviour because stock prices are influenced by many interconnected factors.

The objective was to evaluate whether machine learning could improve forecasting by combining:

* Historical stock market performance
* Macroeconomic indicators
* Engineered trend and momentum features

## Data Sources

### Yahoo Finance

Market data for:

* Apple
* Microsoft
* Nvidia
* Amazon
* Alphabet
* Meta
* Tesla
* Broadcom
* Adobe
* PepsiCo
* Costco
* AMD
* Netflix
* Intel
* Cisco
* Texas Instruments
* Qualcomm
* Applied Materials
* PayPal
* Starbucks

### FRED

Macroeconomic indicators:

* Federal Funds Rate
* Consumer Price Index (CPI)
* Unemployment Rate
* Gross Domestic Product (GDP)
* 10-Year Treasury Yield
* M2 Money Supply

## Data Engineering

### Data Preparation

* Aligned monthly and quarterly macroeconomic data to daily stock market frequency
* Forward-filled GDP values
* Normalised engineered macroeconomic features using Z-score scaling
* Removed redundant variables

### Feature Engineering

Created:

* Stock returns
* Lagged returns
* Lagged macroeconomic indicators
* GDP update flag
* Rolling averages
* Rolling volatility metrics
* Percentage changes in macroeconomic indicators
* NASDAQ rolling trend features

## Models

### Classification Model

Algorithm:

* XGBoost Classifier

Target:

* NASDAQ Direction Tomorrow

Performance:

* Accuracy: 74%
* Bullish F1 Score: 0.78

### Regression Model

Algorithm:

* XGBoost Regressor

Target:

* NASDAQ Return Tomorrow

Performance:

* RMSE: 0.0081
* R²: 0.4609

## Key Findings

* Lagged stock returns contributed more to predictions than macroeconomic indicators.
* NASDAQ rolling return features were the strongest predictors.
* Macroeconomic indicators showed limited influence in short-term daily predictions.
* The classification model performed better than the regression model.
* The regression model performed well during stable market conditions but underestimated extreme rallies and crashes.

## Challenges

* Combining datasets with different reporting frequencies.
* Preventing look-ahead bias in time-series predictions.
* Managing market volatility and sudden price swings.
* Hyperparameter optimisation without overfitting.

## Technologies

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Yahoo Finance API
* FRED API
* Matplotlib
* Seaborn

## Skills Demonstrated

* Machine Learning
* Time Series Analysis
* Feature Engineering
* Model Evaluation
* Hyperparameter Tuning
* Financial Data Analysis
* Data Engineering
* Predictive Analytics

## Results

Successfully developed two predictive models capable of forecasting NASDAQ-100 behaviour using historical stock market and macroeconomic data. The classification model achieved 74% accuracy, while the regression model achieved an RMSE of 0.0081 and explained approximately 46% of return variance.

