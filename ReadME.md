Overview
This project analyzes data from the product_info.csv file, offering insights into product distribution, pricing trends, customer engagement, inventory status, and category segmentation. The analysis uses Python libraries such as Pandas, Matplotlib, and Seaborn to clean, preprocess, and visualize the data.

Project Structure
data/product_info.csv: The main dataset containing product information.
notebooks/Main.ipynb: Jupyter notebook containing all the code, data cleaning, and analysis for this project.
README.md: Project documentation providing an overview, installation instructions, code overview, and next steps.

Installation

Install Required Libraries: This project relies on Python and requires the following libraries:

Pandas
Matplotlib
Seaborn
NumPy

Data Description
The product_info.csv file contains multiple columns relevant to the analysis:

brand: Brand name of the product
loves_count: Number of 'loves' or likes each product received
price: Price of the product
limited_edition, new, online_only, out_of_stock, sephora_exclusive: Boolean indicators for product status and exclusivity
primary_category, secondary_category: Product category classification (e.g., skincare, makeup, hair)
Key Functions in Code
Data Cleaning: Removes columns with over 50% missing values, handles null values, and converts Boolean columns to binary for analysis.
Brand Distribution Analysis: Identifies the top brands by product count.
Customer Engagement Analysis: Analyzes engagement metrics (loves_count, reviews, rating) to identify popular products.
Price Analysis: Compares price distributions across exclusive vs. non-exclusive, online-only vs. in-store, and limited edition vs. regular items.
Inventory Analysis: Analyzes out_of_stock rates by brand, focusing on high-demand items.
Category Segmentation: Breaks down primary and secondary product categories, identifying high-value and popular items within categories.
Sephora-Exclusive Products: Examines out-of-stock rates, price trends, and distribution of exclusive products.

Example Usage
To run the analysis, open the notebook Main.ipynb and execute each cell sequentially. Visualization results will appear inline, offering insights into product data distribution, pricing trends, and customer engagement.

Results
Key findings are documented within the notebook, with visualizations highlighting:

Top-performing brands and most loved products
High-price and high-demand items, especially among Sephora-exclusive and limited-edition products
Category-based breakdowns of product inventory and customer engagement
Next Steps
Potential improvements for future analyses:

Include customer demographic data to segment preferences
Integrate seasonality analysis to predict demand and restocking needs
