# SpaceX Falcon 9 First-Stage Landing Prediction
An End-to-End Data Science Case Study

## 📌 Project Overview
SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because SpaceX can reuse the first stage. Therefore, determining if the first stage will land will help determine the cost of a launch. 

This repository contains a comprehensive, end-to-end Machine Learning case study aimed at predicting whether the Falcon 9 first stage will land successfully.

## 🚀 Key Learning Objectives & Workflow
* **Data Collection & Ingestion:** Leveraged SpaceX API requests and web scraping to build the core dataset.
* **Data Wrangling & EDA:** Handled missing values, engineered features, and performed exploratory analysis using Pandas and SQL queries.
* **Data Visualization:** Built interactive charts using Matplotlib, Seaborn, and Folium maps to spot geographical and payload trends.
* **Machine Learning Pipelines:** Scaled features, split datasets, and trained 4 classification algorithms.
* **Hyperparameter Optimization:** Utilized 10-fold Cross-Validation (`GridSearchCV`) to fine-tune model parameters.

---

## 🛠️ Tech Stack & Libraries
* **Language:** Python 3.13
* **Data Libraries:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn
* **Machine Learning:** Scikit-Learn (`StandardScaler`, `train_test_split`, `GridSearchCV`)
* **Models Tested:** Logistic Regression, Support Vector Machine (SVM), Decision Tree Classifier, K-Nearest Neighbors (KNN)

---

## 📊 Modeling & Evaluation

The core feature matrix $X$ was standardized using `StandardScaler` to bring all metrics (e.g., Payload Mass, Orbit type) onto a comparable scale. The dataset was split into **80% training** and **20% testing** using a fixed `random_state=2` for strict reproducibility.

### Model Comparison Matrix

| Classification Model | Training Accuracy (`best_score_`) | Test Accuracy (`score`) |
| :--- | :---: | :---: |
| **Logistic Regression** | 84.64% | **83.33%** |
| **Support Vector Machine (SVM)** | 84.82% | **83.33%** |
| **K-Nearest Neighbors (KNN)** | 84.82% | **83.33%** |
| **Decision Tree Classifier** | ~84.00% (Variable) | **83.33%** |

### 🔍 Core Findings & Verdict
1. **The 83.33% Tie:** All four optimized classification models achieved an identical accuracy of **83.33% on the test dataset**. 
2. **Sample Limitation:** This exact convergence happens because the test slice consists of a highly limited sample size (18 specific flights). All models correctly predicted exactly 15 out of 18 landings, failing on the exact same corner cases.
3. **Recommendation:** For production deployment, **SVM** or **Logistic Regression** are preferred due to their mathematical stability over Decision Trees, which exhibit higher variance on small datasets.

---

## 📂 Project Structure
```text
├── data/                            # Raw and processed datasets
├── notebooks/                       # Jupyter Notebooks detailing the step-by-step labs
│   ├── 1_Data_Collection.ipynb
│   ├── 2_EDA_with_SQL.ipynb
│   └── 3_Machine_Learning_Prediction.ipynb  <-- Includes final modeling
├── src/                             # Python source scripts (if modularized)
├── README.md                        # Project documentation
└── requirements.txt                 # Dependencies
