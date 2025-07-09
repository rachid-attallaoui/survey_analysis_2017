# analysing_data.py

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ========== SETUP ==========

# Create output folders if they don't exist
os.makedirs("output/charts", exist_ok=True)

# Load data
DATA_PATH = "data/multipleChoiceResponses.csv"
df = pd.read_csv(DATA_PATH, encoding="ISO-8859-1", low_memory=False)

# ========== DATA CLEANING ==========

# Drop metadata row, empty rows/columns
df = df.drop(0).dropna(axis=1, how="all").dropna(axis=0, how="all").reset_index(drop=True)

# Clean salary column
df['CompensationAmount'] = pd.to_numeric(df['CompensationAmount'], errors='coerce')
df = df[df['CompensationAmount'].between(5000, 500000)]
print("Cleaned salary data:\n", df['CompensationAmount'].describe())

# ========== VISUALIZATIONS ==========

def save_plot(fig, filename):
    """Save plot to output/charts/ folder."""
    fig.tight_layout()
    fig.savefig(f"output/charts/{filename}", dpi=300)
    plt.close(fig)

# 1. Salary Distribution
fig1 = plt.figure(figsize=(10, 5))
sns.histplot(df['CompensationAmount'], bins=50, kde=True)
plt.xlim(0, 200000)
plt.title("Salary Distribution")
plt.xlabel("Salary (USD)")
plt.ylabel("Count")
save_plot(fig1, "salary_distribution.png")

# 2. Salary by Education Level
edu_salary = (
    df.groupby("FormalEducation")["CompensationAmount"]
    .median()
    .dropna()
    .sort_values(ascending=False)
)
fig2 = plt.figure(figsize=(12, 6))
sns.barplot(x=edu_salary.values, y=edu_salary.index, palette="viridis")
plt.title("Median Salary by Education Level")
plt.xlabel("Median Salary (USD)")
plt.ylabel("Education Level")
save_plot(fig2, "salary_by_education.png")

# 3. Salary by Job Title
job_salary = (
    df.groupby("CurrentJobTitleSelect")["CompensationAmount"]
    .median()
    .dropna()
    .sort_values(ascending=False)
)
fig3 = plt.figure(figsize=(12, 6))
sns.barplot(x=job_salary.values, y=job_salary.index, palette="magma")
plt.title("Median Salary by Job Title")
plt.xlabel("Median Salary (USD)")
plt.ylabel("Job Title")
save_plot(fig3, "salary_by_jobtitle.png")

# 4. Salary by Country (Top 10)
top_countries = df['Country'].value_counts().head(10).index
df_top_countries = df[df['Country'].isin(top_countries)]
country_salary = (
    df_top_countries.groupby("Country")["CompensationAmount"]
    .median()
    .sort_values(ascending=False)
)
fig4 = plt.figure(figsize=(12, 6))
sns.barplot(x=country_salary.values, y=country_salary.index, palette="coolwarm")
plt.title("Median Salary by Country (Top 10)")
plt.xlabel("Median Salary (USD)")
plt.ylabel("Country")
save_plot(fig4, "salary_by_country.png")

# ========== NOTES ==========
# Some countries may show skewed results due to currency inconsistencies or low sample size.
