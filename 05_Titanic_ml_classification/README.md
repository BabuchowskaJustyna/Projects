## Titanic ML Classification

A short project for classifying Titanic passengers (survived/did not survive) using a Jupyter notebook.

### Contents
- `Titanic_ml_classification.ipynb` — the main notebook with EDA, feature engineering, model training, and evaluation.

### Requirements
- Python 3.9+ (recommended 3.10/3.11)
- pip
- Python packages: numpy, pandas, scikit-learn, matplotlib, seaborn, jupyter

### Data
- If you use the Kaggle Titanic dataset, place the CSV files (e.g., `train.csv`, `test.csv`) in the project directory or adjust paths in the notebook.
- If the notebook downloads or generates data itself, run all cells to reproduce results.

### Typical Notebook Flow
- Exploratory Data Analysis (EDA)
- Data cleaning and feature engineering
- Train/validation split
- Model training
- Metric evaluation

### Results (Summary)
- Model selection: Logistic Regression chosen based on higher validation AUC.
  - Validation comparison: LogReg AUC ≈ 0.868 vs RandomForest AUC ≈ 0.861
  - Final test set: Accuracy ≈ 0.838, AUC ≈ 0.858

