# Student Performance Analysis & Dashboard

## Project Overview

This project explores the relationship between students' academic performance and various academic, lifestyle, and background factors using Exploratory Data Analysis (EDA) and an interactive Streamlit dashboard.

The analysis focuses on identifying patterns and understanding which factors are more strongly associated with students' final grades.

### Research Question

**Are academic factors or lifestyle factors more strongly associated with students' final grades?**

## Dataset

The project uses the **Student Performance Dataset** from the UCI Machine Learning Repository, focusing on Portuguese language performance.

- **Source:** [UCI Student Performance Dataset](https://archive.ics.uci.edu/dataset/320/student+performance)
- **Records:** 649 students
- **Features:** 33 columns
- **Target Variable:** `G3` (Final Grade, 0–20)

The dataset includes information about study habits, previous failures, absences, family background, social activities, and academic performance.

## Tools & Technologies

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Plotly Express
- Streamlit
- Jupyter Notebook

## Project Workflow

### 1. Data Exploration
- Examined dataset structure, data types, and summary statistics.
- Checked for missing values and duplicate records.
- Investigated the distribution of numerical and categorical variables.

### 2. Data Cleaning
- Confirmed that the dataset contained no missing values or duplicate records.
- Investigated outliers using the Interquartile Range (IQR) method.
- Retained plausible absence outliers to preserve potentially useful information.
- Exported the validated dataset for dashboard development.

### 3. Exploratory Data Analysis
- **Univariate Analysis:** Examined grade distributions, study time, and other student characteristics.
- **Bivariate Analysis:** Explored relationships between individual factors and final grades.
- **Multivariate Analysis:** Used correlation analysis to compare multiple factors.

### 4. Interactive Dashboard
Developed a Streamlit dashboard featuring:
- Filters for school, sex, and age.
- Dataset preview and summary statistics.
- Interactive grade distribution and relationship visualizations.
- Academic, lifestyle, background, and previous-grade comparisons.
- Key findings and interpretations.
  
### Dashboard Preview


<img width="777" height="511" alt="image" src="https://github.com/user-attachments/assets/f10e1791-a3ec-4900-86f1-ab735ac516d7" />


## Key Findings

- **Previous academic failures** showed the strongest negative correlation with final grades among the selected academic and lifestyle factors (Spearman r = -0.448).
- **Study time** showed a positive correlation with final grades (r = 0.275).
- **Lifestyle factors**, including going out and free time, generally showed weaker correlations.
- **Parental education** showed positive associations with final grades.
- **Previous grades (G1 and G2)** were strongly associated with final grades (G3).

Overall, the selected academic factors generally showed stronger individual associations with final grades than the lifestyle factors examined.

*These findings represent statistical associations and do not establish causation.*

## How to Run the Dashboard

1. Clone or download this repository.
2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

Make sure `student_performance_clean.csv` is in the same directory as `app.py`.

## Project Files

| File | Description |
|---|---|
| `EDA_Project.ipynb` | Jupyter Notebook containing the full EDA workflow |
| `app.py` | Interactive Streamlit dashboard |
| `student-por.csv` | Original Portuguese student performance dataset |
| `student_performance_clean.csv` | Validated dataset used by Streamlit |

## Dataset Reference

Cortez, P., & Silva, A. (2008). *Using Data Mining to Predict Secondary School Student Performance*. Proceedings of the 5th Future Business Technology Conference.

Dataset available at: https://archive.ics.uci.edu/dataset/320/student+performance
