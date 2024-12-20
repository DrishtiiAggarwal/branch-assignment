import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the dataset
df = pd.read_excel(r"C:\Users\dell\Downloads\loans.xlsx")

# Step 2: Data validation and preprocessing
required_columns = ['USER_ID', 'CREATED_AT', 'USER_LOAN_RANK', 'CREDIT_SCORE', 'AMOUNT_DISBURSED', 'LOAN_STATUS']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

if 'LOAN_TENURE' not in df.columns:
    df['LOAN_TENURE'] = None

df['CREATED_AT'] = pd.to_datetime(df['CREATED_AT'])

# Sort and filter for the most recent loan entries
df_sorted = df.sort_values(by=['USER_ID', 'CREATED_AT'], ascending=[True, False])
last_loans = df_sorted.drop_duplicates(subset=['USER_ID'], keep='first')

# Step 3: Identify defaulters and non-defaulters
defaulters = last_loans[last_loans['LOAN_STATUS'] == 'defaulted']
non_defaulters = last_loans[last_loans['LOAN_STATUS'] != 'defaulted']

# Save defaulters and non-defaulters data for further analysis
defaulters.to_csv("defaulters_list.csv", index=False)
non_defaulters[['USER_ID', 'USER_LOAN_RANK', 'CREDIT_SCORE']].to_csv("non_defaulters_USER_LOAN_RANK_CREDIT_SCORE.csv", index=False)

# Step 4: Performance analysis
## Insights: Credit Score and Loan Rank
USER_LOAN_RANK_analysis = non_defaulters.groupby('USER_LOAN_RANK')['CREDIT_SCORE'].mean().reset_index()
USER_LOAN_RANK_analysis.to_csv("USER_LOAN_RANK_analysis.csv", index=False)

# Step 5: Visualizations
## Loan Rank Distribution (Defaulters vs Non-Defaulters)
defaulters_rank_count = defaulters['USER_LOAN_RANK'].value_counts().sort_index()
non_defaulters_rank_count = non_defaulters['USER_LOAN_RANK'].value_counts().sort_index()
plt.figure(figsize=(12, 6))
plt.bar(defaulters_rank_count.index, defaulters_rank_count.values, alpha=0.7, label="Defaulters")
plt.bar(non_defaulters_rank_count.index, non_defaulters_rank_count.values, alpha=0.7, label="Non-Defaulters")
plt.xlabel("Loan Rank")
plt.ylabel("Count of Users")
plt.title("Number of Loans by Loan Rank (Defaulters vs Non-Defaulters)")
plt.legend()
plt.savefig("loan_rank_distribution.png")
plt.show()

## Average Credit Score by Loan Rank
avg_credit_score = last_loans.groupby('USER_LOAN_RANK')['CREDIT_SCORE'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='USER_LOAN_RANK', y='CREDIT_SCORE', data=avg_credit_score, palette="viridis")
plt.xlabel("Loan Rank")
plt.ylabel("Average Credit Score")
plt.title("Average Credit Score by Loan Rank")
plt.savefig("avg_credit_score_by_rank.png")
plt.show()

## Credit Score Distribution by Loan Status
plt.figure(figsize=(12, 6))
sns.boxplot(x='LOAN_STATUS', y='CREDIT_SCORE', data=last_loans, palette="Set2")
plt.xlabel("Loan Status")
plt.ylabel("Credit Score")
plt.title("Credit Score Distribution by Loan Status")
plt.savefig("credit_score_distribution_by_status.png")
plt.show()

## Scatter Plot: Loan Amount vs Credit Score (Defaulters)
plt.figure(figsize=(12, 6))
sns.scatterplot(x='CREDIT_SCORE', y='AMOUNT_DISBURSED', data=defaulters, alpha=0.7, color="red")
plt.xlabel("Credit Score")
plt.ylabel("Loan Amount")
plt.title("Loan Amount vs Credit Score (Defaulters)")
plt.savefig("loan_amount_vs_credit_score_defaulters.png")
plt.show()

# Additional Analysis
## Loan Amount by Loan Rank (Non-Defaulters)
amount_disbursed_by_rank = non_defaulters.groupby('USER_LOAN_RANK')['AMOUNT_DISBURSED'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='USER_LOAN_RANK', y='AMOUNT_DISBURSED', data=amount_disbursed_by_rank, palette="Blues_d")
plt.xlabel("Loan Rank")
plt.ylabel("Average Loan Amount")
plt.title("Average Loan Amount by Loan Rank (Non-Defaulters)")
plt.savefig("avg_loan_amount_by_rank.png")
plt.show()

## Credit Score Range and Default Rates
defaulters['CREDIT_SCORE_RANGE'] = pd.cut(defaulters['CREDIT_SCORE'], bins=[0, 300, 600, 750, 850], labels=['Very Poor', 'Poor', 'Good', 'Excellent'])
defaulters_credit_range = defaulters['CREDIT_SCORE_RANGE'].value_counts().reset_index()
defaulters_credit_range.columns = ['CREDIT_SCORE_RANGE', 'COUNT']
plt.figure(figsize=(12, 6))
sns.barplot(x='CREDIT_SCORE_RANGE', y='COUNT', data=defaulters_credit_range, palette='muted')
plt.xlabel("Credit Score Range")
plt.ylabel("Number of Defaulters")
plt.title("Default Counts by Credit Score Range")
plt.savefig("default_counts_by_credit_score_range.png")
plt.show()

# Save insights and export visuals
print("Analysis complete. Generated CSVs and visualizations saved.")
