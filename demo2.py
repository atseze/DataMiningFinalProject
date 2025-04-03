import pandas as pd

# Sample Donor dataset
donor_data = {
    'UserID': [1, 2, 3],
    'Gender': ['M', 'F', 'M'],
    'State': ['CA', 'TX', 'NY'],
    'BirthDate': ['1980-01-01', '1990-05-10', '1985-09-23'],
    'ReferralSource': ['Friend', 'Online', 'Event']
}
donor_df = pd.DataFrame(donor_data)

# Sample Payment dataset
payment_data = {
    'TransID': [101, 102, 103, 104, 105],
    'UserID': [1, 2, 1, 3, 1],
    'PaymentDate': ['2023-01-01', '2023-01-15', '2023-02-01', '2023-02-10', '2023-03-01'],
    'PaymentAmount': [100, 200, 150, 300, 50],
    'SupportType': ['Recurring', 'One-time', 'Recurring', 'One-time', 'Recurring']
}
payment_df = pd.DataFrame(payment_data)

# Calculate the number of records and sum of payments for each UserID in the Payment dataset
payment_summary = payment_df.groupby('UserID').agg(
    NumPayments=('TransID', 'count'),
    TotalPayment=('PaymentAmount', 'sum')
).reset_index()

# Merge the summary back into the Donor dataset
donor_df = donor_df.merge(payment_summary, on='UserID', how='left')

# Fill NaN values with 0 for users with no payment records
donor_df['NumPayments'] = donor_df['NumPayments'].fillna(0).astype(int)
donor_df['TotalPayment'] = donor_df['TotalPayment'].fillna(0)

from scipy.stats import ttest_ind

male_data = donor_df[donor_df['Gender'] == 'M']
female_data = donor_df[donor_df['Gender'] == 'F']

# Perform t-tests for NumPayments and TotalPayment
num_payments_test = ttest_ind(male_data['NumPayments'], female_data['NumPayments'], equal_var=False)
total_payment_test = ttest_ind(male_data['TotalPayment'], female_data['TotalPayment'], equal_var=False)

# Print results
print("T-test for NumPayments (Gender Dependency):")
print(f"Statistic: {num_payments_test.statistic}, p-value: {num_payments_test.pvalue}")

print("\nT-test for TotalPayment (Gender Dependency):")
print(f"Statistic: {total_payment_test.statistic}, p-value: {total_payment_test.pvalue}")


#print(donor_df)
