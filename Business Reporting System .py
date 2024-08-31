#!/usr/bin/env python
# coding: utf-8

# # Business Reporting System: A Data Analysis and Visualization Project
# This project involves both a detailed data analysis in Jupyter Notebook and an interactive Tableau dashboard. The Tableau dashboard is designed to allow stakeholders to explore key metrics and trends, supporting data-driven decision-making.
# 
# ## Key Objectives: 
# - Analyze sales performance across different segments and countries.
# - Identify key trends in pricing, costs, and profitability.
# - Provide actionable recommendations based on data insights to support business decision-making.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


# Import Data set to see structure
file_path = r"C:\Users\AKKem\OneDrive\Desktop\Data Analysis Modules\Projects\Project 5\Business_Reporting_System\financials.csv"
company_df = pd.read_csv(file_path)


# In[3]:


# Display first few rows of the dataset
company_df.head()


# In[4]:


# Get information about data types and non-null values
company_df.info()


# ## Data Cleaning and Validation
# The dataset will be cleaned by removing duplicates, handling missing values, and converting data types. Special attention was given to ensuring that monetary values were correctly formatted and numerical fields were accurately converted. This process is essential for maintaining data integrity and ensuring accurate analysis.
# 

# In[5]:


# Show the number of missing values per column if applicable
company_df.isnull().sum()


# In[6]:


# Identify and Remove Duplicate Rows
company_df.drop_duplicates(inplace=True)


# In[7]:


# Drop unnessecary columns 
company_df.drop(columns = ['Month Number'],axis=1,inplace=True)

company_df.head()


# In[8]:


# Determine all unique Segments within the dataset 
company_df['Segment'].unique()


# In[9]:


# Determine how many values per Segment 
company_df['Segment'].value_counts()


# In[10]:


# Change the names of all the columns 

df = company_df.rename(columns = {
    'Segment': 'segment',
    'Country': 'country',
    ' Product ': 'product',
    ' Discount Band ': 'discount_band',
    ' Units Sold ': 'units_sold',
    ' Manufacturing Price ': 'manufacturing_price',
    ' Sale Price ': 'sale_price',
    ' Gross Sales ': 'gross_sales',
    ' Discounts ': 'discounts',
    '  Sales ': 'sales',
    ' COGS ': 'cogs',
    ' Profit ': 'profit',
    'Date': 'date',
    'Month Number': 'month_number',
    ' Month Name ': 'month_name',
    'Year': 'year'
})

df.head(10)


# In[11]:


print(df.dtypes)


# In[12]:


# Columns that should be treated as strings
string_columns = ["units_sold", "manufacturing_price", "sale_price", "gross_sales", "discounts", "sales", "cogs", "profit"]

# Convert the relevant columns to string, clean them, and convert to numeric
for i in string_columns:
    if df[i].dtype == 'object':  # Check if the column is of object type
        df[i] = df[i].str.replace("$", "", regex=False)  # Remove dollar sign
        df[i] = df[i].str.replace(",", "", regex=False)  # Remove commas
        df[i] = df[i].str.replace("(", "", regex=False)  # Remove opening parenthesis
        df[i] = df[i].str.replace(")", "", regex=False)  # Remove closing parenthesis
        df[i] = df[i].str.replace("-", "0", regex=False)  # Replace dashes with 0
        df[i] = df[i].astype(float)  # Convert to float
        df[i] = df[i].astype(int)  # Convert to integer

# Display Cleaned Dataframe
df.head()


# In[13]:


# Convert date column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')


# In[14]:


# Convert month_name column to categorical format
df['month_name'] = df['month_name'].astype(category')


# In[15]:


# List of columns to handle outliers
columns = ['units_sold', 'manufacturing_price', 'sale_price', 'gross_sales', 'discounts', 'sales', 'cogs', 'profit']

# Loop through each column to handle outliers
for column in columns:
    # Calculate Q1, Q3, and IQR
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    # Determine lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Identify outliers
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    
    # Print outliers for the current column
    print(f'Outliers in column {column}:')
    print(outliers)

    # Optionally, handle outliers (e.g., cap the values)
    df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)


# In[16]:


# Export the cleaned and processed data for use in Tableau
df.to_csv('cleaned_financial_data.csv', index=False)


# # Exploratory Data Analysis

# In[17]:


# Box Plots to visualize the distribution and detect outliers

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12, 6))

for i, column in enumerate(['units_sold', 'manufacturing_price', 'sale_price', 'gross_sales', 'discounts', 'sales', 'cogs', 'profit']):
    plt.subplot(2, 4, i+1)
    sns.boxplot(df[column])
    plt.title(column)

plt.tight_layout()
plt.show()


# In[18]:


# Histograms for understanding the distribution of numeric variables
df[['units_sold', 'manufacturing_price', 'sale_price', 'gross_sales', 'discounts', 'sales', 'cogs', 'profit']].hist(figsize=(12, 10))
plt.show()


# ## Sales Performance Analysis
# Understanding sales performance across different segments is crucial for targeting marketing efforts and allocating resources effectively. The following visualization shows total sales by segment, helping to identify which segments contribute most to revenue.
# 

# In[19]:


# Sales by Segment
plt.figure(figsize=(10, 6))
sns.barplot(x='segment', y='sales', data=df, palette='Blues_d')
plt.title('Total Sales by Segment')
plt.xticks(rotation=45)
plt.xlabel('Segment')
plt.ylabel('Total Sales')
plt.show()


# In[20]:


# Units Sold by Country
plt.figure(figsize=(12, 8))
sns.barplot(x='country', y='units_sold', data=df, palette='Blues_d')
plt.title('Units Sold by Country')
plt.xticks(rotation=45)
plt.xlabel('Country')
plt.ylabel('Units Sold')
plt.show()


# In[21]:


# Revenue and Profit Trends
plt.figure(figsize=(12, 6))
sns.lineplot(x='date', y='gross_sales', data=df, label='Gross Sales', color='blue')
sns.lineplot(x='date', y='profit', data=df, label='Profit', color='green')
plt.title('Revenue and Profit Trends Over Time')
plt.xlabel('Date')
plt.ylabel('Amount')
plt.legend()
plt.xticks(rotation=45)
plt.show()


# ## Sales Performance Analysis
# 
# ### Summary of Findings:
# - **Government Segment Dominance**: The Government segment is the largest contributor to total sales, indicating strong market penetration.
# - **Potential Growth Areas**: The Small Business segment shows lower sales but may have untapped potential, suggesting a need for targeted strategies.
# 
# ### Recommendations:
# - **Focus Marketing on Government Segment**: Given its dominance, allocate more resources to reinforce this segment’s performance.
# - **Explore Small Business Opportunities**: Develop specific marketing campaigns and product offerings tailored to the Small Business segment to drive growth.
# 

# ## Pricing and Cost Analysis
# 
# Pricing and cost analysis are critical components of business strategy and financial management. Effective pricing strategies ensure that products are competitively priced while maximizing profit margins. By analyzing the relationship between manufacturing costs and sale prices, businesses can identify opportunities to optimize profitability and maintain a competitive edge in the market.

# In[22]:


# Price vs. Profit
plt.figure(figsize=(10, 6))
sns.scatterplot(x='sale_price', y='profit', data=df, palette='Blues_d')
plt.title('Price vs. Profit')
plt.xlabel('Sale Price')
plt.ylabel('Profit')
plt.show()


# In[23]:


# Manufacturing Price vs. Sale Price
plt.figure(figsize=(10, 6))
sns.scatterplot(x='manufacturing_price', y='sale_price', data=df, palette='Blues_d')
plt.title('Manufacturing Price vs. Sale Price')
plt.xlabel('Manufacturing Price')
plt.ylabel('Sale Price')
plt.show()


# ### Summary of Findings:
# - **Price vs. Profit**: The scatter plot indicates a positive correlation between sale price and profit. Higher sale prices generally result in higher profits, as expected. However, there is a clustering of data points at specific price levels, suggesting standard pricing practices or product tiers.
# - **Manufacturing Price vs. Sale Price**: The scatter plot shows that sale prices are typically higher than manufacturing prices, which is necessary for maintaining profitability. There is a broad range of sale prices even for similar manufacturing costs, indicating potential price variability based on market factors or product positioning.
# 
# ### Recommendations:
# - **Optimize Pricing Strategies**: Review the clustering of sale prices to understand why certain price points are favored. Consider if there’s room to adjust pricing strategies to maximize profit, particularly for products that are not hitting the higher profit margins.
# - **Review Cost Management**: Although the sale prices generally exceed manufacturing costs, analyze the products with lower sale price margins to see if cost reductions or pricing adjustments could improve profitability.
# - **Targeted Product Pricing**: Consider introducing differentiated pricing strategies for products with similar manufacturing costs but varying sale prices to ensure that each product’s price aligns with its perceived market value.
# You can add this markdown directly under your "Pricing and Cost Analysis" section in your Jupyter

# ## Discount Impact Analysis
# 
# Discount impact analysis is crucial for understanding how discounting strategies affect sales, revenue, and profitability. Discounts can drive customer behavior, increase sales volume, and clear inventory, but they also directly impact profit margins. By analyzing the effectiveness of various discount bands, businesses can determine the optimal discount levels that maximize sales without eroding profitability.

# In[24]:


# Discounts vs. Sales
# Calculate total discounts by discount band
discounts_by_band = df.groupby('discount_band')['discounts'].sum()

# Plot pie chart
plt.figure(figsize=(10, 8))
plt.pie(discounts_by_band, labels=discounts_by_band.index, autopct='%1.1f%%', colors=sns.color_palette('Blues_d', len(discounts_by_band)))
plt.title('Discounts Distribution by Discount Band')
plt.show()


# In[25]:


# Discount Band Performance
plt.figure(figsize=(12, 8))
sns.barplot(x='discount_band', y='sales', data=df, palette='Blues_d')
plt.title('Sales by Discount Band')
plt.xlabel('Discount Band')
plt.ylabel('Sales')
plt.show()


# ### Summary of Findings:
# - **Sales by Discount Band**: The bar plot indicates that discounts do have a significant impact on sales. However, the highest sales are observed in the "Low" and "None" discount bands, suggesting that significant discounts may not always be necessary to drive sales.
# - **Discount Distribution by Band**: The pie chart shows that the majority of discounts fall into the "High" and "Medium" bands, indicating that substantial discounts are frequently applied. This raises questions about the overall pricing strategy and whether such high discounts are sustainable in the long term.
# 
# ### Recommendations:
# - **Reevaluate Discount Strategies**: Given that lower discount bands still drive significant sales, consider reducing the frequency or depth of high discounts. This could help in maintaining profitability without sacrificing sales volume.
# - **Targeted Discount Campaigns**: Focus high discounts on specific products or market segments where they are most effective, rather than applying them broadly.
# - **Monitor Discount Effectiveness**: Continuously analyze the impact of different discount bands on sales and profitability to refine discount strategies over time.
# 

# ## Product Performance
# Product performance analysis is crucial for understanding which products drive revenue and where opportunities exist for growth. It helps in making informed decisions about resource allocation, marketing focus, and product development, ultimately contributing to the company's profitability and market position.

# In[26]:


# Product Contribution
plt.figure(figsize=(12, 8))
sns.barplot(x='product', y='sales', data=df, palette='Blues_d')
plt.title('Total Sales by Product')
plt.xticks(rotation=45)
plt.xlabel('Product')
plt.ylabel('Total Sales')
plt.show()


# In[27]:


# Product Sales by Segment
plt.figure(figsize=(12, 8))
sns.barplot(x='product', y='units_sold', hue='segment', data=df, palette='Blues_d')
plt.title('Units Sold by Product and Segment')
plt.xticks(rotation=45)
plt.xlabel('Product')
plt.ylabel('Units Sold')
plt.legend(title='Segment')
plt.show()


# ## Product Performance
# 
# ### Summary of Findings:
# - **Total Sales by Product**: The bar plot shows the distribution of total sales across different products. The products appear to have a relatively even distribution of sales, with slight variations that suggest some products are slightly more popular or better-performing than others.
# - **Units Sold by Product and Segment**: The stacked bar plot provides insights into the units sold for each product across different market segments. This detailed breakdown shows that certain products perform better in specific segments, indicating varying levels of market penetration and customer preference.
# 
# ### Recommendations:
# - **Focus on High-Performing Products**: Identify the products with the highest sales and consider focusing marketing and development efforts on these products to further boost their performance.
# - **Segment-Specific Strategies**: Tailor marketing and sales strategies to specific segments where certain products are particularly successful. For instance, if a product performs well in the Government segment but not in Small Business, a targeted approach can be developed to increase penetration in the underperforming segments.
# - **Evaluate Underperforming Products**: Products with consistently lower sales should be evaluated to determine if they need re-positioning, pricing adjustments, or even discontinuation if they do not align with market demand.
# 

# ## Monthly and Yearly Trends
# Analyzing monthly and yearly trends is crucial for understanding the timing of sales and profit fluctuations. This analysis allows businesses to anticipate seasonal changes, allocate resources more effectively, and make informed decisions to sustain long-term growth.
# 

# In[28]:


# Monthly Sales and Profit Trends
plt.figure(figsize=(12, 6))
sns.lineplot(x='month_name', y='sales', data=df, label='Sales', color='blue')
sns.lineplot(x='month_name', y='profit', data=df, label='Profit', color='green')
plt.title('Monthly Sales and Profit Trends')
plt.xlabel('Month')
plt.ylabel('Amount')
plt.legend()
plt.xticks(rotation=45)
plt.show()


# In[29]:


# Yearly Performance Comparison
plt.figure(figsize=(12, 6))
sns.barplot(x='year', y='sales', data=df, palette='Blues_d')
plt.title('Yearly Sales Comparison')
plt.xlabel('Year')
plt.ylabel('Sales')
plt.show()


# ### Summary of Findings:
# - **Monthly Sales and Profit Trends**: The line plot illustrates fluctuations in sales and profit throughout the year. The data suggests seasonal trends, with certain months consistently outperforming others in terms of sales and profit.
# - **Yearly Sales Comparison**: The bar chart comparing sales between 2013 and 2014 shows an overall increase in sales year-over-year, indicating positive growth.
# 
# ### Recommendations:
# - **Leverage Seasonal Trends**: Identify the factors driving higher sales and profit during peak months and develop strategies to replicate this success during lower-performing months.
# - **Sustain Yearly Growth**: Continue to analyze yearly trends to ensure sustained growth. Explore what contributed to the increased sales in 2014 and apply those insights to future strategies.

# ## Cost and Profitability Analysis
# Cost and profitability analysis is crucial for identifying the factors that drive or hinder financial performance. By understanding the relationship between costs, sales, and profits, businesses can make informed decisions to optimize resource allocation, pricing strategies, and cost management practices, ultimately leading to sustained profitability.
# 

# In[30]:


# COGS vs. Profit
plt.figure(figsize=(10, 6))
sns.scatterplot(x='cogs', y='profit', data=df, palette='Blues_d')
plt.title('COGS vs. Profit')
plt.xlabel('COGS')
plt.ylabel('Profit')
plt.show()


# In[31]:


# Gross Sales vs. Profit
plt.figure(figsize=(10, 6))
sns.scatterplot(x='gross_sales', y='profit', data=df, palette='Blues_d')
plt.title('Gross Sales vs. Profit')
plt.xlabel('Gross Sales')
plt.ylabel('Profit')
plt.show()


# ### Summary of Findings:
# - **COGS vs. Profit**: The scatter plot indicates a wide range of COGS (Cost of Goods Sold) values relative to profit. There is a concentration of data points where low COGS correlates with varying profit levels, suggesting that while lower costs generally lead to higher profitability, other factors also influence profit.
# - **Gross Sales vs. Profit**: The scatter plot shows a positive correlation between gross sales and profit. However, the spread of data points indicates that some high gross sales do not always correspond to equally high profits, pointing to potential inefficiencies or areas for cost management improvement.
# 
# ### Recommendations:
# - **Optimize Cost Management**: Focus on reducing COGS where possible to enhance profitability, particularly in areas where high costs do not translate into proportional profits.
# - **Analyze High-Gross-Low-Profit Scenarios**: Investigate instances where high gross sales result in lower-than-expected profits. This could uncover inefficiencies in pricing, discounting, or cost management that can be addressed to improve overall profitability.
