
# Exoplanet Classification using Machine Learning

## Project Summary

Developed and compared five machine learning models to classify celestial objects observed by NASA's Kepler mission into:

* False Positives
* Candidate Exoplanets
* Confirmed Exoplanets

The project combined planetary observations from the Kepler Objects of Interest (KOI) dataset with stellar characteristics from the Kepler Input Catalog (KIC).

## Business Problem

The Kepler mission generated extremely large datasets containing thousands of observed celestial objects.

Manual validation of exoplanets is resource-intensive and time-consuming.

The objective was to evaluate whether machine learning could automate classification while maintaining high levels of accuracy.

## Data Sources

### NASA Exoplanet Archive

Dataset:

* Kepler Objects of Interest (KOI)

Contents:

* Planetary observations
* Transit characteristics
* Orbital measurements

### Kepler Input Catalog (KIC)

Contents:

* Stellar properties
* Star characteristics
* Physical measurements

## Data Engineering

### Dataset Preparation

* Filtered KIC data to matching Kepler IDs
* Merged KOI and KIC datasets
* Removed duplicate and redundant variables
* Treated missing values using median imputation
* Removed highly correlated features
* Treated outliers using:

  * Log transformations
  * Winsorisation
* Applied feature scaling where required

### Feature Engineering

Created:

#### Planet-Star Ratio

Measures planet size relative to host star.

#### Depth per Planet Radius

Measures transit depth relative to planet size.

#### Duration Ratio

Measures transit duration relative to orbital period.

## Models Evaluated

### XGBoost

Accuracy:

* 92.8%

### Random Forest

Accuracy:

* 91.9%

### Support Vector Machine

Accuracy:

* 89.8%

### Multi-Layer Perceptron

Accuracy:

* 89.5%

### K-Nearest Neighbours

Accuracy:

* 81.0%

## Key Findings

* Tree-based models significantly outperformed distance-based models.
* XGBoost produced the highest overall accuracy.
* Random Forest achieved very similar performance to XGBoost.
* KNN struggled with the dataset's dimensionality.
* Stellar characteristics provided valuable additional information beyond planetary observations alone.

## Challenges

* Large-scale data integration.
* Significant class imbalance.
* Missing values across multiple variables.
* High dimensionality.
* Feature redundancy and multicollinearity.

## Technologies

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Random Forest
* SVM
* KNN
* MLP
* SMOTE
* Matplotlib
* Seaborn

## Skills Demonstrated

* Machine Learning
* Classification Modelling
* Feature Engineering
* Data Cleaning
* Class Imbalance Handling
* Model Comparison
* Hyperparameter Tuning
* Scientific Data Analysis

## Results

Successfully trained and evaluated five machine learning models to classify exoplanets. XGBoost achieved the strongest performance with 92.8% accuracy, demonstrating that machine learning can effectively support astronomical object classification.
