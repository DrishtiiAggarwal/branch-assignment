import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel(r"C:\Users\dell\Downloads\loans.xlsx")

required_columns = ['USER_ID', 'CREATED_AT', 'USER_LOAN_RANK', 'CREDIT_SCORE', 'AMOUNT_DISBURSED', 'LOAN_STATUS']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

if 'LOAN_TENURE' not in df.columns:
    df['LOAN_TENURE'] = None

df['CREATED_AT'] = pd.to_datetime(df['CREATED_AT'])

df_sorted = df.sort_values(by=['USER_ID', 'CREATED_AT'], ascending=[True, False])
last_loans = df_sorted.drop_duplicates(subset=['USER_ID'], keep='first')

#Identify defaulters and non-defaulters
defaulters = last_loans[last_loans['LOAN_STATUS'] == 'defaulted']
non_defaulters = last_loans[last_loans['LOAN_STATUS'] != 'defaulted']

defaulters.to_csv("defaulters_list.csv", index=False)
non_defaulters[['USER_ID', 'USER_LOAN_RANK', 'CREDIT_SCORE']].to_csv("non_defaulters_USER_LOAN_RANK_CREDIT_SCORE.csv", index=False)

#Performance analysis
USER_LOAN_RANK_analysis = non_defaulters.groupby('USER_LOAN_RANK')['CREDIT_SCORE'].mean().reset_index()
USER_LOAN_RANK_analysis.to_csv("USER_LOAN_RANK_analysis.csv", index=False)

#Visualizations
## Loan Rank Distribution (Defaulters vs Non-Defaulters)
defaulters_rank_count = defaulters['USER_LOAN_RANK'].value_counts().sort_index()
non_defaulters_rank_count = non_defaulters['USER_LOAN_RANK'].value_counts().sort_index()

defaulters_color = "red"
non_defaulters_color = "blue"
plt.figure(figsize=(12, 6))
plt.xlim([0, 30])
plt.bar(defaulters_rank_count.index, defaulters_rank_count.values, alpha=0.7, color=defaulters_color, label="Defaulters")
plt.bar(non_defaulters_rank_count.index, non_defaulters_rank_count.values, alpha=0.7, color=non_defaulters_color, label="Non-Defaulters")
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

#Average Loan Amount by Loan Rank (Defaulters vs Non-Defaulters
#for defaulters
defaulters_avg_amount = defaulters.groupby('USER_LOAN_RANK')['AMOUNT_DISBURSED'].mean().reset_index()
defaulters_avg_amount['CATEGORY'] = 'Defaulters'

#for non-defaulters
non_defaulters_avg_amount = non_defaulters.groupby('USER_LOAN_RANK')['AMOUNT_DISBURSED'].mean().reset_index()
non_defaulters_avg_amount['CATEGORY'] = 'Non-Defaulters'

#comparison
combined_avg_amount = pd.concat([defaulters_avg_amount, non_defaulters_avg_amount])

plt.figure(figsize=(12, 6))
sns.barplot(x='USER_LOAN_RANK', y='AMOUNT_DISBURSED', hue='CATEGORY', data=combined_avg_amount, palette={'Defaulters': '#FF6F61', 'Non-Defaulters': '#2B7A78'})
plt.xlabel("Loan Rank")
plt.ylabel("Average Loan Amount")
plt.title("Average Loan Amount by Loan Rank (Defaulters vs Non-Defaulters)")
plt.legend(title="Category")
plt.savefig("avg_loan_amount_by_rank_defaulters_vs_non_defaulters.png")
plt.show()


## Credit Score Range and Default Rates
defaulters['CREDIT_SCORE_RANGE'] = pd.cut(defaulters['CREDIT_SCORE']*100, bins=[0, 40, 60, 80,100 ], labels=['Very Poor(0.0-0.39)', 'Poor(0.40-0.59)', 'Good(0.60-0.79)', 'Excellent(0.80-1)'])
defaulters_credit_range = defaulters['CREDIT_SCORE_RANGE'].value_counts().reset_index()
defaulters_credit_range.columns = ['CREDIT_SCORE_RANGE', 'COUNT']
plt.figure(figsize=(12, 6))
sns.barplot(x='CREDIT_SCORE_RANGE', y='COUNT', data=defaulters_credit_range, palette='muted')
plt.xlabel("Credit Score Range")
plt.ylabel("Number of Defaulters")
plt.title("Default Counts by Credit Score Range")
plt.savefig("default_counts_by_credit_score_range.png")
plt.show()

print("Analysis complete.")
