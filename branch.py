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

#to get the most recent loan entries
df_sorted = df.sort_values(by=['USER_ID', 'CREATED_AT'], ascending=[True, False])

#Droping duplicates 
last_loans = df_sorted.drop_duplicates(subset=['USER_ID'], keep='first')


defaulters = last_loans[last_loans['LOAN_STATUS'] == 'defaulted']
defaulters.to_csv("defaulters_list.csv", index=False)


non_defaulters = last_loans[last_loans['LOAN_STATUS'] != 'defaulted']
non_defaulters[['USER_ID', 'USER_LOAN_RANK', 'CREDIT_SCORE']].to_csv("non_defaulters_USER_LOAN_RANK_CREDIT_SCORE.csv", index=False)

USER_LOAN_RANK_analysis = non_defaulters.groupby('USER_LOAN_RANK')['CREDIT_SCORE'].mean().reset_index()
USER_LOAN_RANK_analysis.to_csv("USER_LOAN_RANK_analysis.csv", index=False)

print("Data cleaning and CSV generation complete.")

defaulters_rank_count = defaulters['USER_LOAN_RANK'].value_counts().sort_index()
non_defaulters_rank_count = non_defaulters['USER_LOAN_RANK'].value_counts().sort_index()

#Plotting the counts
plt.figure(figsize=(12, 6))
plt.bar(defaulters_rank_count.index, defaulters_rank_count.values, alpha=0.7, label="Defaulters")
plt.bar(non_defaulters_rank_count.index, non_defaulters_rank_count.values, alpha=0.7, label="Non-Defaulters")
plt.xlabel("Loan Rank")
plt.ylabel("Count of Users")
plt.title("Number of Loans by Loan Rank (Defaulters vs Non-Defaulters)")
plt.legend()
plt.show()

#Average CREDIT_SCORE across different loan ranks
avg_credit_score = last_loans.groupby('USER_LOAN_RANK')['CREDIT_SCORE'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='USER_LOAN_RANK', y='CREDIT_SCORE', data=avg_credit_score, palette="viridis")
plt.xlabel("Loan Rank")
plt.ylabel("Average Credit Score")
plt.title("Average Credit Score by Loan Rank")
plt.show()

#Analyze anomalies or patterns in CREDIT_SCORE and LOAN_STATUS
plt.figure(figsize=(12, 6))
sns.boxplot(x='LOAN_STATUS', y='CREDIT_SCORE', data=last_loans, palette="Set2")
plt.xlabel("Loan Status")
plt.ylabel("Credit Score")
plt.title("Credit Score Distribution by Loan Status")
plt.show()

#Loan rank distribution among defaulters (Bar chart)
defaulters_rank_count = defaulters['USER_LOAN_RANK'].value_counts().sort_index()
plt.figure(figsize=(12, 6))
plt.bar(defaulters_rank_count.index, defaulters_rank_count.values, color='orange', alpha=0.8)
plt.xlabel("Loan Rank")
plt.ylabel("Count of Defaulters")
plt.title("Loan Rank Distribution Among Defaulters")
plt.show()

#Scatter plot of AMOUNT_DISBURSED vs. CREDIT_SCORE for defaulters
plt.figure(figsize=(12, 6))
sns.scatterplot(x='CREDIT_SCORE', y='AMOUNT_DISBURSED', data=defaulters, alpha=0.7, color="red")
plt.xlabel("Credit Score")
plt.ylabel("Loan Amount")
plt.title("Loan Amount vs. Credit Score (Defaulters)")
plt.show()

#Average CREDIT_SCORE by USER_LOAN_RANK (Line graph)
avg_credit_score_by_rank = non_defaulters.groupby('USER_LOAN_RANK')['CREDIT_SCORE'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(x='USER_LOAN_RANK', y='CREDIT_SCORE', data=avg_credit_score_by_rank, marker='o', color='green')
plt.xlabel("Loan Rank")
plt.ylabel("Average Credit Score")
plt.title("Average Credit Score by Loan Rank (Non-Defaulters)")
plt.grid(True)
plt.show()

#Loan amounts across USER_LOAN_RANK (Bar chart)
AMOUNT_DISBURSED_by_rank = non_defaulters.groupby('USER_LOAN_RANK')['AMOUNT_DISBURSED'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='USER_LOAN_RANK', y='AMOUNT_DISBURSED', data=AMOUNT_DISBURSED_by_rank, palette="Blues_d")
plt.xlabel("Loan Rank")
plt.ylabel("Average Loan Amount")
plt.title("Average Loan Amount by Loan Rank (Non-Defaulters)")
plt.show()

#Average Loan Amount and Credit Score
avg_AMOUNT_DISBURSED_defaulters = defaulters['AMOUNT_DISBURSED'].mean()
avg_AMOUNT_DISBURSED_non_defaulters = non_defaulters['AMOUNT_DISBURSED'].mean()
avg_credit_score_defaulters = defaulters['CREDIT_SCORE'].mean()
avg_credit_score_non_defaulters = non_defaulters['CREDIT_SCORE'].mean()

print(f"Average Loan Amount - Defaulters: {avg_AMOUNT_DISBURSED_defaulters}")
print(f"Average Loan Amount - Non-Defaulters: {avg_AMOUNT_DISBURSED_non_defaulters}")
print(f"Average Credit Score - Defaulters: {avg_credit_score_defaulters}")
print(f"Average Credit Score - Non-Defaulters: {avg_credit_score_non_defaulters}")

#Overlayed Histograms for CREDIT_SCORE
plt.figure(figsize=(12, 6))
sns.histplot(defaulters['CREDIT_SCORE'], color='red', label='Defaulters', kde=True, bins=30, alpha=0.6)
sns.histplot(non_defaulters['CREDIT_SCORE'], color='green', label='Non-Defaulters', kde=True, bins=30, alpha=0.6)
plt.xlabel("Credit Score")
plt.ylabel("Density")
plt.title("Credit Score Distribution: Defaulters vs Non-Defaulters")
plt.legend()
plt.show()

#Box Plot of AMOUNT_DISBURSED for Defaulters and Non-Defaulters
combined_data = pd.concat([
    defaulters[['AMOUNT_DISBURSED']].assign(Group='Defaulters'),
    non_defaulters[['AMOUNT_DISBURSED']].assign(Group='Non-Defaulters')
])
sns.boxplot(x='Group', y='AMOUNT_DISBURSED', data=combined_data, palette='Set2')
plt.xlabel("Group")
plt.ylabel("Loan Amount")
plt.title("Loan Amount Distribution: Defaulters vs Non-Defaulters")
plt.show()

#Additional Plots
#Average Loan Amount of Defaulters per Loan Rank
avg_loan_default_rank = defaulters.groupby('USER_LOAN_RANK')['AMOUNT_DISBURSED'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='USER_LOAN_RANK', y='AMOUNT_DISBURSED', data=avg_loan_default_rank, palette='coolwarm')
plt.xlabel("Loan Rank")
plt.ylabel("Average Loan Amount (Defaulters)")
plt.title("Average Loan Amount of Defaulters per Loan Rank")
plt.show()

#Average Number of Defaulters per Credit Score Range
defaulters['CREDIT_SCORE_RANGE'] = pd.cut(defaulters['CREDIT_SCORE'], bins=[0, 300, 600, 750, 850], labels=['Very Poor', 'Poor', 'Good', 'Excellent'])
defaulters_credit_range = defaulters['CREDIT_SCORE_RANGE'].value_counts().reset_index()
defaulters_credit_range.columns = ['CREDIT_SCORE_RANGE', 'COUNT']
plt.figure(figsize=(12, 6))
sns.barplot(x='CREDIT_SCORE_RANGE', y='COUNT', data=defaulters_credit_range, palette='muted')
plt.xlabel("Credit Score Range")
plt.ylabel("Number of Defaulters")
plt.title("Average Number of Defaulters per Credit Score Range")
plt.show()

#Number of People Defaulted at Each Loan Rank
defaulters_rank_count = defaulters['USER_LOAN_RANK'].value_counts().reset_index()
defaulters_rank_count.columns = ['USER_LOAN_RANK', 'COUNT']
plt.figure(figsize=(12, 6))
sns.barplot(x='USER_LOAN_RANK', y='COUNT', data=defaulters_rank_count, palette='plasma')
plt.xlabel("Loan Rank")
plt.ylabel("Number of Defaulters")
plt.title("Number of People Defaulted at Each Loan Rank")
plt.show()
