import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

Monday_df = pd.read_excel("monday_voucher_data.xlsx")
Tuesday_df = pd.read_excel("tuesday_voucher_data.xlsx")
Wednesday_df = pd.read_excel("wednesday_voucher_data.xlsx")
Thursday_df = pd.read_excel("thursday_voucher_data.xlsx")
Friday_df = pd.read_excel("friday_voucher_data.xlsx")
Saturday_df = pd.read_excel("saturday_voucher_data.xlsx")
Sunday_df = pd.read_excel("sunday_voucher_data.xlsx")

df = pd.concat([Monday_df , Tuesday_df , Wednesday_df , Thursday_df , Friday_df , Saturday_df , Sunday_df], axis=0)

# print(df)

df["New Transaction ID"] = range(1, len(df["Transaction ID"])+1)
# print(df)

df = df.drop(columns = ["Transaction ID"])
df = df.set_index("New Transaction ID")
df = df.dropna(how = "any")
# print(df)

def split_basket(string):
    items = string.split(",")
    stripped_items = [item.strip() for item in items]
    return stripped_items

df["Basket"] = df["Basket"].apply(split_basket)

df["Payment Method"] = df["Payment Method"].str.upper()

# Function to convert each item in a list to uppercase
def uppercase_list_items(basket_items):
    return [item.upper() for item in basket_items] if isinstance(basket_items, list) else basket_items

# Apply the function to each row in the 'basket' column
df['Basket'] = df['Basket'].apply(uppercase_list_items)

df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# print(df.head(5))
# print(df.describe())
# print(df.info())

exploded_data_df = df.explode("Basket", ignore_index=False) 
# print(exploded_data_df["Basket"])

df.to_excel("Our_Cleaned_Data.xlsx")
# print(df.describe())


# ...................................................................................................................
# 1st Question:             How many sales were made on each payment type? Ticked
# ...................................................................................................................

# print(df["Payment Method"].value_counts())

# Payment Method
# DEBIT            165
# CASH             102
# CREDIT            67
# VOUCHER           33
# MOBILE WALLET     31


# ..................................................................................................................
# 2nd Question:          How many unique items were paid for by each payment type?
# ..................................................................................................................

# print(df["Total Items"].sum())  # 1514 
# print(df.groupby("Payment Method")["Total Items"].sum()) 

# Payment Method
# CASH             395.0
# CREDIT           246.0
# DEBIT            650.0
# MOBILE WALLET     97.0
# VOUCHER          126.0

# print(df["Cost"].sum())

# # Counting each item by each payment method
# # Standardize 'Payment Method' values to title case for consistency
# df['Payment Method'] = df['Payment Method'].str.title()

# # Get all unique items across baskets
# unique_items = set(item for basket in df['Basket'] for item in basket)

# # Initialize an empty dictionary to store counts
# item_payment_counts = {}

# # Loop over each unique item and payment method
# for item in unique_items:
#     item_payment_counts[item] = {}
#     for method in df['Payment Method'].unique():
#         # Count orders that include the item and use the payment method
#         count = df[(df['Payment Method'] == method) & 
#                      (df['Basket'].apply(lambda items: item in items))].shape[0]
#         item_payment_counts[item][method] = count

# # Display the results in a DataFrame for readability
# item_payment_counts_df = pd.DataFrame(item_payment_counts).T
# # print(item_payment_counts_df)

# Cash  Debit  Mobile Wallet  Credit  Voucher
# Croissant         8     11              3       3        1
# Muffin            4     14              1       2        2
# Tea              42     74              8      30       12
# Stroopwafel       6     12              2       1        1
# Toast             6     10              0       3        1
# Hot Chocolate    45     69             17      33       15
# Latte            48     66             11      30       18
# Buttered Roll     7     12              2       4        2
# Panini            3      9              2       2        1
# Cappuccino       47     70              8      35       18
# Mocha            44     80              9      21       20
# Gift Voucher      0      7              1       3        0
# Americano        46     66             13      24       10


# .................................................................................................................
# 3rd Question:        What percentage of income made came from vouchers?
# .................................................................................................................

# print(df.groupby("Payment Method")["Cost"].sum())
# Payment Method
# Cash              684.2
# Credit            519.5
# Debit            1237.8
# Mobile Wallet     198.4
# Voucher           228.7


# Group by 'Payment Method' and calculate total income per method
# income_by_payment = df.groupby('Payment Method')['Cost'].sum()

# # Plot the pie chart
# plt.figure(figsize=(8, 8))
# plt.pie(income_by_payment, labels=income_by_payment.index, autopct='%1.1f%%', startangle=140)
# plt.title("Percentage of Income by Payment Method")
# plt.show()




#...................................................................................................................
# 4th Question:             For each days of week, how many orders were made by each payment method?
#...................................................................................................................

# # Group by 'Day of the Week' and 'Payment Method', then count orders
# orders_by_day_payment = df.groupby(['Day', 'Payment Method']).size().unstack(fill_value=0)

# # Sort the days of the week in order
# days_order = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
# # print(days_order)
# orders_by_day_payment = orders_by_day_payment.reindex(days_order)
# # orders_by_day_payment_percentage = orders_by_day_payment.div(orders_by_day_payment.sum(axis=1), axis=0) * 100

# # Plot a stacked horizontal bar chart
# orders_by_day_payment.plot(kind='barh', stacked=True, figsize=(10, 7))

# # Add labels and title
# plt.xlabel("Number of Orders")
# plt.ylabel("Day of the Week")
# plt.title("Number of Orders by Payment Method and Day of the Week")
# plt.legend(title="Payment Method")
# plt.show()


# ..................................................................................................................
# 5th Question:                What is average spend per transaction per each payment type?
# ..................................................................................................................

# print(df.groupby("Payment Method")["Cost"].mean())
# Payment Method
# CASH             6.707843
# CREDIT           7.753731
# DEBIT            7.501818
# MOBILE WALLET    6.400000
# VOUCHER          6.930303


mean_spend_payment_method_df = df.groupby("Payment Method")["Cost"].mean()
color_bars = ['#800080', '#008000', '#00008b', '#add8e6', '#ffa500']

bars = plt.bar(mean_spend_payment_method_df.index, mean_spend_payment_method_df.values, color=color_bars)

# Adding labels on each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

plt.title("Average Spend per Transaction per Payment Type")
plt.xlabel("Payment Method")
plt.ylabel("Spend £")
plt.show()



# ..................................................................................................................
# 6th Question:                   When do the vouchers begin to pay for themselves?
# ..................................................................................................................


# 33 vouchers per week make the income 228.7 £. 
# We bought them for 33 * 0.91 to 33 * 2 (30 to 66) £. +25/3 >>>> 38 to 74 £ 
# So they worth it. 
# 1051 for the software x * (228.7 - 56) = 1051 >>>>>> after 6 weeks, using VOUCHERS can benefit the store. 

# 












# ..................................................................................................................
# 7th Question:                                   Is there any outlier?                
# ..................................................................................................................

# plt.boxplot(df["Cost"], vert = 0)
# plt.title("The Week Sales")
# plt.xlabel("Cost (£)")
# plt.show()

# Cathrine
# count_df = df[df["Cost"].between(-3.75 , 17.46)] # for counting the number of cost values between 2 values: -3.75 , 17.46
# print(count_df["Cost"].count())

# outliers_count_df = df[df["Cost"] > 17.45]
# print(outliers_count_df["Cost"].value_counts())

# Cost
# 30.0    3
# 25.0    3
# 20.0    1


# echo "# vouchers" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/FerSar8765/vouchers.git
# git push -u origin main