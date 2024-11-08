import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

pd.set_option('display.max_columns', None)

product_data = pd.read_csv('product_info.csv')
product_data.head(4)

## DESCRIPTIVE STATISTICS 
product_data.info()

product_data.isnull().sum()

threshold = len(product_data) * 0.5
product_cleaned = product_data.dropna(thresh=threshold, axis=1)

product_cleaned= product_cleaned.dropna()

product_cleaned.info()

print ("\nUnique values :  \n",product_cleaned.nunique())

### Change type for some column to boolan

product_cleaned['limited_edition'] = product_cleaned['limited_edition'].astype('bool')
product_cleaned['new'] = product_cleaned['new'].astype('bool')
product_cleaned['online_only'] = product_cleaned['online_only'].astype('bool')
product_cleaned['out_of_stock'] = product_cleaned['out_of_stock'].astype('bool')
product_cleaned['sephora_exclusive'] = product_cleaned['sephora_exclusive'].astype('bool')

product_cleaned[['limited_edition', 'new', 'online_only', 'out_of_stock', 'sephora_exclusive']]

## DATA VISUALIZATION and STATISTICS  

product_cleaned.describe()

## Top Thirty brands 

top_brands =  product_cleaned['brand_name'].value_counts().reset_index().head(30)
top_brands.columns = ['brand_name', 'count']
top_brands.head(5)

# Plotting the top 30 brands by product count
top_brands.iloc[:: -1].plot(kind='barh',x='brand_name', color='darkblue',figsize=(10, 8))
plt.title("Top 30 Brands by Product Count")
plt.xlabel("Brand")
plt.ylabel("Number of Products")
plt.tight_layout()
plt.show()

## Customer Engagement - Top Products by loves_count, reviews and Ratings

#top fifty product and brands base on reviews 
top_products_reviews = product_cleaned[['product_name', 'brand_name', 'reviews']].sort_values(by='reviews', ascending=False).head(50).reset_index()
top_products_reviews.head(5)

#top fifty products and brands base on loves_count
top_products_loves = product_cleaned[['product_name', 'brand_name', 'loves_count']].sort_values(by='loves_count', ascending=False).head(50).reset_index()
top_products_loves.head(5)

##top fifty products and brand  base on rating
top_products_rating = product_cleaned[['product_name', 'brand_name', 'rating']].sort_values(by='rating', ascending=False)\
    .head(50).reset_index(drop=True)
top_products_rating.head(15)

# Select the top 15 highest-rated products
top_15_products = top_products_rating.head(15)

# Plot the data
plt.figure(figsize=(10, 8))
plt.barh(top_15_products['product_name'], top_15_products['rating'], color='#4682B4', edgecolor='black')
plt.xlabel('Rating')
plt.ylabel('Product Name')
plt.title('Top 15 Highest Rated Products')
plt.gca().invert_yaxis()  # Invert y-axis to show highest rating at the top
plt.tight_layout()
plt.show()

#bottom fifty products base on love_counts
bottom_products_love = product_cleaned[['product_name', 'brand_name', 'loves_count']].sort_values(by='loves_count')\
    .head(50).reset_index(drop=True)
bottom_products_love.head(5)

#bottom fifty product base on reviews 
bottom_products_reviews = product_cleaned[['product_name', 'brand_name', 'reviews']].sort_values(by='reviews')\
    .head(50).reset_index(drop=True)
bottom_products_reviews.head(5)

## Price Analysis

product_cleaned['price_usd'].describe()

expensive_products = product_cleaned[['product_name', 'brand_name', 'price_usd']].sort_values(by='price_usd', ascending=False )\
    .head(50).reset_index(drop=True)
expensive_products.head(10)

expensive_products[['brand_name']].value_counts()

# Select the top 10 most expensive products for plotting
top_20_expensive = expensive_products.head(20)

# Plot the data
plt.figure(figsize=(10, 6))
plt.barh(top_20_expensive['product_name'], top_20_expensive['price_usd'], color='#FF8C00', edgecolor='black')
plt.xlabel('Price (USD)')
plt.ylabel('Product Name')
plt.title('Top 20 Most Expensive Products')
plt.gca().invert_yaxis()  # Invert y-axis to show most expensive at the top
plt.tight_layout()
plt.show()

## Price Distribution 

product_cleaned['price_usd'].plot(kind='hist', bins=30, color='darkgreen')
plt.title("Price Distribution")
plt.xlabel("Price (USD)")
plt.ylabel("Frequency")
plt.show()

# Set up the figure with subplots
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# First subplot: Countplot for brand names in the most expensive products
sns.countplot(data=expensive_products, x='brand_name', ax=axes[0], palette='viridis')
axes[0].set_title("Count of Most Expensive Products by Brand")
axes[0].set_xlabel("Brand")
axes[0].set_ylabel("Count")
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)

# Second subplot: Histogram for price distribution
sns.histplot(data=expensive_products, x='price_usd', ax=axes[1], bins=10, color='#FF8C00', kde=True)
axes[1].set_title("Price Distribution of Most Expensive Products")
axes[1].set_xlabel("Price (USD)")
axes[1].set_ylabel("Frequency")

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()

## Inventory analysis

inventory = product_cleaned[['product_name','brand_name','price_usd','new','limited_edition','online_only','out_of_stock','sephora_exclusive']]
inventory

# Count out-of-stock items by brand
out_of_stock_brands = inventory[inventory['out_of_stock'] == True]['brand_name'].value_counts().head(20)

# Plot the top brands with out-of-stock items
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
out_of_stock_brands.plot(kind='bar', color='salmon', edgecolor='black')
plt.title("Top Brands with Out of Stock Items")
plt.xlabel("Brand")
plt.ylabel("Out of Stock Count")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Filter data for exclusive and limited edition items
exclusive_limited = inventory[(inventory['limited_edition'] == True) | (inventory['sephora_exclusive'] == True)]

# Plot distribution of prices for exclusive and limited edition items
plt.figure(figsize=(10, 6))
sns.histplot(exclusive_limited['price_usd'], bins=15, color='teal', kde=True)
plt.title("Price Distribution of Exclusive & Limited Edition Products")
plt.xlabel("Price (USD)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Separate online-only and in-store products
online_only = inventory[inventory['online_only'] == True]
in_store = inventory[inventory['online_only'] == False]

# Compare average prices
avg_online_price = online_only['price_usd'].mean()
avg_in_store_price = in_store['price_usd'].mean()

print(f"Average Price of Online Only Products: ${avg_online_price:.2f}")
print(f"Average Price of In-Store Products: ${avg_in_store_price:.2f}")

# Filter new products and calculate their average price
new_products = inventory[inventory['new'] == True]
existing_products = inventory[inventory['new'] == False]

# Calculate average prices
avg_new_price = new_products['price_usd'].mean()
avg_existing_price = existing_products['price_usd'].mean()

print(f"Average Price of New Products: ${avg_new_price:.2f}")
print(f"Average Price of Existing Products: ${avg_existing_price:.2f}")

## Sephora-Exclusive

# Count the number of exclusive and non-exclusive products
sephora_counts = inventory['sephora_exclusive'].value_counts().rename({True: 'Exclusive', False: 'Non-Exclusive'})

# Plot the counts
plt.figure(figsize=(8, 6))
sns.barplot(x=sephora_counts.index, y=sephora_counts.values, palette='pastel')
plt.title("Count of Sephora-Exclusive vs. Non-Exclusive Products")
plt.xlabel("Product Type")
plt.ylabel("Number of Products")
plt.show()

# Calculate percentages
sephora_percent = (sephora_counts / sephora_counts.sum()) * 100

# Plot the percentages
plt.figure(figsize=(8, 6))
sns.barplot(x=sephora_percent.index, y=sephora_percent.values, palette='pastel')
plt.title("Percentage of Sephora-Exclusive vs. Non-Exclusive Products")
plt.xlabel("Product Type")
plt.ylabel("Percentage (%)")
plt.show()

# Separate exclusive and non-exclusive products
exclusive_products = inventory[inventory['sephora_exclusive'] == True]
non_exclusive_products = inventory[inventory['sephora_exclusive'] == False]

# Plot the price distributions
plt.figure(figsize=(12, 6))
sns.histplot(exclusive_products['price_usd'], color='gold', label='Exclusive', kde=True, stat="density", linewidth=0)
sns.histplot(non_exclusive_products['price_usd'], color='skyblue', label='Non-Exclusive', kde=True, stat="density", linewidth=0, alpha=0.6)
plt.title("Price Distribution: Sephora-Exclusive vs. Non-Exclusive Products")
plt.xlabel("Price (USD)")
plt.ylabel("Density")
plt.legend()
plt.show()

# Count exclusive products by brand
top_exclusive_brands = exclusive_products['brand_name'].value_counts().head(10)

# Plot the top brands
plt.figure(figsize=(12, 6))
sns.barplot(x=top_exclusive_brands.values, y=top_exclusive_brands.index, palette='viridis')
plt.title("Top 10 Brands with Most Sephora-Exclusive Products")
plt.xlabel("Number of Exclusive Products")
plt.ylabel("Brand")
plt.tight_layout()
plt.show()

# Calculate out-of-stock rates for exclusive and non-exclusive products
out_of_stock_exclusive = exclusive_products['out_of_stock'].mean() * 100
out_of_stock_non_exclusive = non_exclusive_products['out_of_stock'].mean() * 100

# Prepare data for plotting
out_of_stock_data = pd.Series({
    'Exclusive': out_of_stock_exclusive,
    'Non-Exclusive': out_of_stock_non_exclusive
})

# Plot the out-of-stock rates
plt.figure(figsize=(8, 6))
sns.barplot(x=out_of_stock_data.index, y=out_of_stock_data.values, palette='coolwarm')
plt.title("Out-of-Stock Rates: Sephora-Exclusive vs. Non-Exclusive Products")
plt.xlabel("Product Type")
plt.ylabel("Out-of-Stock Rate (%)")
plt.show()

# Count limited edition exclusive products by brand
limited_exclusive = exclusive_products[exclusive_products['limited_edition'] == True]['brand_name'].value_counts().head(10)

# Plot the data
plt.figure(figsize=(12, 6))
sns.barplot(x=limited_exclusive.values, y=limited_exclusive.index, palette='magma')
plt.title("Top 10 Brands with Most Limited Edition Sephora-Exclusive Products")
plt.xlabel("Number of Limited Edition Products")
plt.ylabel("Brand")
plt.tight_layout()
plt.show()

# Calculate average prices
avg_price_exclusive = exclusive_products['price_usd'].mean()
avg_price_non_exclusive = non_exclusive_products['price_usd'].mean()

# Print the results
print(f"Average Price of Sephora-Exclusive Products: ${avg_price_exclusive:.2f}")
print(f"Average Price of Non-Exclusive Products: ${avg_price_non_exclusive:.2f}")

# Count online-only exclusive products
online_exclusive = exclusive_products[exclusive_products['online_only'] == True].shape[0]
in_store_exclusive = exclusive_products[exclusive_products['online_only'] == False].shape[0]

# Prepare data for plotting
online_exclusive_data = pd.Series({
    'Online-Only': online_exclusive,
    'In-Store': in_store_exclusive
})

# Plot the distribution
plt.figure(figsize=(8, 6))
sns.barplot(x=online_exclusive_data.index, y=online_exclusive_data.values, palette='Set2')
plt.title("Distribution of Sephora-Exclusive Products: Online vs. In-Store")
plt.xlabel("Sales Channel")
plt.ylabel("Number of Products")
plt.show()

# Summary statistics for exclusive products
exclusive_summary = exclusive_products.describe()

# Display the summary
print("Summary Statistics for Sephora-Exclusive Products:")
print(exclusive_summary)


## Product Category

product_cleaned['primary_category'].value_counts().iloc[::-1].plot(kind= 'barh', color='maroon')

plt.title('Primary Product Category')
plt.xlabel('Count')
plt.tight_layout()
plt.show()

## Secondary Product category

product_cleaned['secondary_category'].value_counts().iloc[::-1].plot(kind='barh', color='lightcoral',figsize=(12, 8))

plt.title('Secondary Product Category')
plt.xlabel('Count')
plt.tight_layout()
plt.show()

## skincare analysis
## Expensive skincare 

brands_skincare = product_cleaned.query('primary_category == "Skincare" and secondary_category != "High Tech Tools"').groupby(['brand_id', 'brand_name'])['price_usd'].mean().sort_values(ascending=True)

ten_lowest = product_cleaned.query('primary_category == "Skincare" and secondary_category != "High Tech Tools"').groupby(['brand_id', 'brand_name'])['price_usd'].mean().sort_values(ascending=True).head(20)
ten_lowest = ten_lowest.iloc[::-1]
ten_highest = product_cleaned.query('primary_category == "Skincare" and secondary_category != "High Tech Tools"').groupby(['brand_id', 'brand_name'])['price_usd'].mean().sort_values(ascending=True).tail(20)

# Plot the skincare analysis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 10), sharex=True)

# Plot the 20 lowest-priced skincare brands
ten_lowest.plot(kind='barh', color='#4CAF50', ax=ax1, edgecolor='black')
ax1.set_title('20 Lowest Priced Skincare Brands')
ax1.set_xlabel('Average Price (USD)')
ax1.set_ylabel('Brand')

# Plot the 20 highest-priced skincare brands
ten_highest.plot(kind='barh', color='#FF5722', ax=ax2, edgecolor='black')
ax2.set_title('20 Highest Priced Skincare Brands')
ax2.set_xlabel('Average Price (USD)')
ax2.set_ylabel('')

# Adjust layout for readability
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))


makeup_price = product_cleaned[['product_name', 'brand_name', 'primary_category', 'price_usd', 'secondary_category']].query('primary_category == "Skincare" and secondary_category !="High Tech Tools"').nlargest(20, 'price_usd')
makeup_plot = makeup_price.drop(columns=['primary_category', 'secondary_category']).groupby(['brand_name', 'product_name'])['price_usd'].max().sort_values(ascending=False).iloc[::-1]

plt.figure(figsize=(10, 8))

# Plot the data
makeup_plot.plot(kind='barh', color='#FF6347', edgecolor='black')

# Add titles and labels
plt.title("Top 20 Highest Priced Skincare Products (Excluding High Tech Tools)")
plt.xlabel("Price (USD)")
plt.ylabel("Brand and Product")

# Tight layout for readability
plt.tight_layout()

# Show the plot
plt.show()


## Most_Love Skincare

plt.figure(figsize=(10, 6))


skincare_loved_product = product_cleaned.query('primary_category == "Skincare" and secondary_category !="High Tech Tools"').groupby(['brand_name', 'product_name'])['loves_count'].sum().sort_values(ascending=False).head(20).iloc[::-1]
skincare_loved_product.plot(kind='barh',  color='lightsalmon', edgecolor='dimgrey', width=0.7)

plt.title('20 Most Loved Skincare Products', fontdict={'fontsize': 16})
plt.xlabel('Loves Count')
plt.ylabel('Product Name')


plt.show()

## Makeup Brand Analysis

brands_makeup = product_cleaned.query('primary_category == "Makeup"') \
                           .groupby(['brand_id', 'brand_name'])['price_usd'].mean()

# Get the 20 lowest and 20 highest average-priced makeup brands
twenty_lowest_makeup = brands_makeup.sort_values(ascending=True).head(20).iloc[::-1]  # Reversed for better plotting order
twenty_highest_makeup = brands_makeup.sort_values(ascending=True).tail(20)

# Set up a figure with subplots for side-by-side comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 10), sharex=True)

# Plot the 20 lowest-priced makeup brands
twenty_lowest_makeup.plot(kind='barh', color='#8A2BE2', ax=ax1, edgecolor='black')
ax1.set_title('20 Lowest Priced Makeup Brands')
ax1.set_xlabel('Average Price (USD)')
ax1.set_ylabel('Brand')

# Plot the 20 highest-priced makeup brands
twenty_highest_makeup.plot(kind='barh', color='#FF4500', ax=ax2, edgecolor='black')
ax2.set_title('20 Highest Priced Makeup Brands')
ax2.set_xlabel('Average Price (USD)')
ax2.set_ylabel('')

# Adjust layout for better readability
plt.tight_layout()
plt.show()

## most love MakeUp product

plt.figure(figsize=(10, 8))

makeup_loved_product = product_cleaned.query('primary_category == "Makeup"').groupby(['brand_name', 'product_name'])['loves_count'].sum().sort_values(ascending=False).head(20).iloc[::-1]
makeup_loved_product.plot(kind='barh', color='darkslateblue', edgecolor='white', width=0.7)

plt.title('20 Most Loved Makeup Products', fontdict={'fontsize': 16})
plt.xlabel('Loves Count')
plt.ylabel('Product Name')


plt.show()

## most expensive makeUp product

plt.figure(figsize=(10, 6))


makeup_price = product_cleaned[['product_name', 'brand_name', 'primary_category', 'price_usd']].query('primary_category == "Makeup"').nlargest(20, 'price_usd')
makeup_plot = makeup_price.drop(columns=['primary_category']).groupby(['brand_name', 'product_name'])['price_usd'].max().sort_values(ascending=False).iloc[::-1]


makeup_plot.plot(kind='barh', color='indigo', edgecolor='white', width=0.7)
plt.title('20 Most Expensive Makeup Products', fontdict={'fontsize': 16})
plt.xlabel('Price USD')
plt.ylabel('Product Name')


plt.show()

## Hair Product Analysis 

brands_hair = product_cleaned.query('primary_category == "Hair" and secondary_category == "Hair Styling & Treatments" and secondary_category != "Tools" and secondary_category != "Value & Gift Sets"')\
                    .groupby(['brand_id', 'brand_name'])['price_usd'].mean().sort_values(ascending=True)

twenty_lowest_hair = product_cleaned.query('primary_category == "Hair" and secondary_category == "Hair Styling & Treatments" and secondary_category != "Tools" and secondary_category != "Value & Gift Sets"')\
                    .groupby(['brand_id', 'brand_name'])['price_usd'].mean().sort_values(ascending=True).head(20).iloc[::-1]
twenty_highest_hair = product_cleaned.query('primary_category == "Hair" and secondary_category == "Hair Styling & Treatments" and secondary_category != "Tools" and secondary_category != "Value & Gift Sets"')\
                    .groupby(['brand_id', 'brand_name'])['price_usd'].mean().sort_values(ascending=True).tail(20)


# Create a subplot with 1 row and 2 columns
fig, axs = plt.subplots(1, 2, figsize=(14, 6))


axs[0].barh(twenty_highest_hair.index.get_level_values('brand_name'), twenty_highest_hair.values, color='orange', edgecolor='dimgrey')
axs[0].set_xlabel('Average Price (USD)')
axs[0].set_ylabel('Brand Name')
axs[0].set_title('20 Most Expensive Hair Product Brands')


axs[1].barh(twenty_lowest_hair.index.get_level_values('brand_name'), twenty_lowest_hair.values, color='lightblue', edgecolor='dimgrey')
axs[1].set_xlabel('Average Price (USD)')
axs[1].set_ylabel('Brand Name')
axs[1].set_title('20 Most Affordable Hair Product Brands')


plt.tight_layout()
plt.show()


## most loved hair product

plt.figure(figsize=(10, 6))

df_avg_brands_hair = product_cleaned.query('primary_category == "Hair" and secondary_category == "Hair Styling & Treatments" and secondary_category != "Tools" and secondary_category != "Value & Gift Sets"')\
                    .groupby(['brand_name', 'product_name'])['loves_count'].sum().sort_values(ascending=False).head(20).iloc[::-1]
df_avg_brands_hair.plot(kind='barh', color='dimgrey', edgecolor='white', width=0.7)


plt.title('20 Most Loved Hair Products', fontdict={'fontsize': 16})
plt.xlabel('Loves Count')
plt.ylabel('Brand Name')


plt.show()

## Most expensive hair product

plt.figure(figsize=(10, 8))


hair_product_price = product_cleaned[['product_name', 'brand_name', 'primary_category', 'price_usd', 'secondary_category']].query('primary_category == "Hair" and secondary_category == "Hair Styling & Treatments" and secondary_category != "Tools" and secondary_category != "Value & Gift Sets"').nlargest(20, 'price_usd')
hair_product_plot = hair_product_price.drop(columns=['primary_category', 'secondary_category']).groupby(['brand_name', 'product_name'])['price_usd'].max().sort_values(ascending=False).iloc[::-1]


hair_product_plot.plot(kind='barh', color='darkgrey', edgecolor='dimgrey', width=0.7)
plt.title('20 Most Expensive Hair Products', fontdict={'fontsize': 16})
plt.xlabel('Price USD')
plt.ylabel('Product Name')


plt.show()

## Fragrance Product Analysis

brands_fragrance = product_cleaned.query('primary_category == "Fragrance"').groupby(['brand_id', 'brand_name'])['price_usd'].mean().sort_values(ascending=True)

twenty_lowest_fragrance = product_cleaned.query('primary_category == "Fragrance"').groupby(['brand_id', 'brand_name'])['price_usd'].mean().sort_values(ascending=True).head(20).iloc[::-1]
twenty_highest_fragrance = product_cleaned.query('primary_category == "Fragrance"').groupby(['brand_id', 'brand_name'])['price_usd'].mean().sort_values(ascending=True).tail(20)


# Create a subplot with 1 row and 2 columns
fig, axs = plt.subplots(1, 2, figsize=(14, 6))


axs[0].barh(twenty_highest_fragrance.index.get_level_values('brand_name'), twenty_highest_fragrance.values, color='orange', edgecolor='dimgrey')
axs[0].set_xlabel('Average Price (USD)')
axs[0].set_ylabel('Brand Name')
axs[0].set_title('20 Most Expensive Fragrance Brands')


axs[1].barh(twenty_lowest_fragrance.index.get_level_values('brand_name'), twenty_lowest_fragrance.values, color='lightblue', edgecolor='dimgrey')
axs[1].set_xlabel('Average Price (USD)')
axs[1].set_ylabel('Brand Name')
axs[1].set_title('20 Most Affordable Fragrance Brands')


plt.tight_layout()
plt.show()

## Most Loved Fragrances

plt.figure(figsize=(10, 8))

df_fragrance_loves = product_cleaned.query('primary_category == "Fragrance"').groupby(['brand_name', 'product_name'])['loves_count'].sum().sort_values(ascending=False).head(20).iloc[::-1]

df_fragrance_loves.plot(kind='barh', color='mediumpurple', edgecolor='black', width=0.7)

plt.title('20 Most Loved Fragrances', fontdict={'fontsize': 16})
plt.xlabel('"Loves" Count')
plt.ylabel('Brand Name')


plt.show()

## Most Expensive Fragrance

plt.figure(figsize=(10, 8))


fragrance_price = product_cleaned[['product_name', 'brand_name', 'primary_category', 'price_usd']].query('primary_category == "Fragrance"').nlargest(20, 'price_usd')
fragrance_plot = fragrance_price.drop(columns=['primary_category']).groupby(['brand_name', 'product_name'])['price_usd'].max().sort_values(ascending=False).iloc[::-1]


fragrance_plot.plot(kind='barh', color='rebeccapurple', edgecolor='black', width=0.7)
plt.title('20 Most Expensive Fragrances', fontdict={'fontsize': 16})
plt.xlabel('Price USD')
plt.ylabel('Product Name')
plt.xlim(250)


plt.show()


