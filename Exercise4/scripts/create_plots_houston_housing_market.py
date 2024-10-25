import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Get the absolute directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the data folder
file_path = os.path.join(script_dir, "../data", "houston_housing_market_2024.csv")

# Load the Houston Housing Market dataset
housing_data = pd.read_csv(file_path)

def clean_up_data():
    # Sort data to prioritize 'Houston' for duplicate zip codes
    housing_data_sorted = housing_data.sort_values(by=['zipcode', 'city'], ascending=[True, False])
    # Drop duplicates based on 'zipcode', keeping the first occurrence (which is Houston if available)
    cleaned_housing_data = housing_data_sorted.drop_duplicates(subset=['zipcode'], keep='first')

    # Normalize city names by converting them to lowercase to avoid case sensitivity issues
    cleaned_housing_data['city'] = cleaned_housing_data['city'].str.lower()
    return cleaned_housing_data

# Display the first few rows and data info to understand the structure
# housing_data_info = housing_data.info()
# housing_data_head = housing_data.head()

# Removing outliers for the 'average_price_per_sqft' by applying the IQR method for each city
def remove_outliers_by_city(df, column):
    """Removes outliers within each city based on the IQR for the specified column."""
    cleaned_data = pd.DataFrame()
    for city, group in df.groupby('city'):
        q1 = group[column].quantile(0.25)
        q3 = group[column].quantile(0.75)
        iqr = q3 - q1
        # Define the bounds for non-outliers
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        # Filter the group to only include non-outliers
        group_no_outliers = group[(group[column] >= lower_bound) & (group[column] <= upper_bound)]
        cleaned_data = pd.concat([cleaned_data, group_no_outliers])
    return cleaned_data

def create_scatter_plots():
    # 1. Scatter Plot: Average Price vs Average Price per Square Foot
    plt.figure(figsize=(10, 6))
    plt.scatter(cleaned_housing_data['average_price'], cleaned_housing_data['average_price_per_sqft'], color='blue', alpha=0.7)
    plt.title('Average Price vs Average Price per Square Foot')
    plt.xlabel('Average Price ($)')
    plt.ylabel('Average Price per Sq Ft ($)')
    plt.tight_layout()
    plt.show()

    # 2. Scatter Plot: Total Listings vs Average Days on Market
    plt.figure(figsize=(10, 6))
    plt.scatter(cleaned_housing_data['total_listings'], cleaned_housing_data['average_days_on_market'], color='green', alpha=0.7)
    plt.title('Total Listings vs Average Days on Market')
    plt.xlabel('Total Listings')
    plt.ylabel('Average Days on Market')
    plt.tight_layout()
    plt.show()

    # 3. Scatter Plot: Average Price per Square Foot vs Average Days on Market
    plt.figure(figsize=(10, 6))
    plt.scatter(cleaned_housing_data['average_price_per_sqft'], cleaned_housing_data['average_days_on_market'], color='purple', alpha=0.7)
    plt.title('Average Price per Square Foot vs Average Days on Market')
    plt.xlabel('Average Price per Sq Ft ($)')
    plt.ylabel('Average Days on Market')
    plt.tight_layout()
    plt.show()

def create_bar_plots():
    # 1. Horizontal Bar Plot: Total Listings per City
    # Group the data by city and sum the total listings
    grouped_data_corrected = cleaned_housing_data.groupby('city')['total_listings'].sum().reset_index()
    # Sort by total listings to make the plot more readable
    grouped_data_corrected = grouped_data_corrected.sort_values(by='total_listings', ascending=False)

    plt.figure(figsize=(10, 12))
    sns.barplot(x='total_listings', y='city', data=grouped_data_corrected, palette="Blues_d")
    plt.title('Total Listings per City (Corrected)')
    plt.xlabel('Total Listings')
    plt.ylabel('City')
    plt.tight_layout()
    plt.show()

    # 2. Bar Plot: Average Price per City
    grouped_avg_price = cleaned_housing_data.groupby('city')['average_price'].mean().reset_index()
    grouped_avg_price = grouped_avg_price.sort_values(by='average_price', ascending=False)

    plt.figure(figsize=(10, 12))
    sns.barplot(x='average_price', y='city', data=grouped_avg_price, palette="Greens_d")
    plt.title('Average Price per City')
    plt.xlabel('Average Price ($)')
    plt.ylabel('City')
    plt.tight_layout()
    plt.show()

    # 3. Bar Plot: Average Days on Market per City
    grouped_days_on_market = cleaned_housing_data.groupby('city')['average_days_on_market'].mean().reset_index()
    grouped_days_on_market = grouped_days_on_market.sort_values(by='average_days_on_market', ascending=False)

    plt.figure(figsize=(10, 12))
    sns.barplot(x='average_days_on_market', y='city', data=grouped_days_on_market, palette="Oranges_d")
    plt.title('Average Days on Market per City')
    plt.xlabel('Average Days on Market')
    plt.ylabel('City')
    plt.tight_layout()
    plt.show()

def create_box_plot():
    # 4. Box Plot: Price per Sqft by City
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=cleaned_housing_data, x='city', y='average_price_per_sqft')
    plt.title("Box Plot of Price per Sqft by City")
    plt.xticks(rotation=45)
    plt.show()

def create_box_plot_no_outliers():
    # Apply the function to remove outliers based on 'average_price_per_sqft'
    houston_housing_no_outliers = remove_outliers_by_city(cleaned_housing_data, 'average_price_per_sqft')

    # Replotting the box plot without outliers to observe the cleaned data
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=houston_housing_no_outliers, x='city', y='average_price_per_sqft')
    plt.title("Box Plot of Price per Sqft by City (Outliers Removed)")
    plt.xticks(rotation=45)
    plt.show()

def create_pie_charts():
    # Pie Chart 1: Share of Listings by City (Top 10 Cities with Others)
    city_counts = cleaned_housing_data['city'].value_counts()
    top_10_cities = city_counts.nlargest(10)
    other_cities_count = city_counts.sum() - top_10_cities.sum()
    top_10_cities['Others'] = other_cities_count
    plt.figure(figsize=(8, 8))
    plt.pie(top_10_cities, labels=top_10_cities.index, autopct='%1.1f%%', startangle=140)
    plt.title("Share of Listings by City (Top 10 Cities with Others)")
    plt.show()

    # Pie Chart 2: Market Share of Listings by Zipcode (Top 10 Zip Codes with Others)
    zipcode_listing_counts = cleaned_housing_data.groupby('zipcode')['total_listings'].sum()
    top_10_zipcodes = zipcode_listing_counts.nlargest(10)
    other_zipcode_count = zipcode_listing_counts.sum() - top_10_zipcodes.sum()
    top_10_zipcodes['Others'] = other_zipcode_count
    plt.figure(figsize=(8, 8))
    plt.pie(top_10_zipcodes, labels=top_10_zipcodes.index, autopct='%1.1f%%', startangle=140)
    plt.title("Market Share of Listings by Zip Code (Top 10 with Others)")
    plt.show()

    # Pie Chart 3: Average Price Distribution by City (Top 10 Cities with Others)
    city_price_averages = cleaned_housing_data.groupby('city')['average_price'].mean()
    top_10_city_prices = city_price_averages.nlargest(10)
    other_city_price = city_price_averages.sum() - top_10_city_prices.sum()
    top_10_city_prices['Others'] = other_city_price
    plt.figure(figsize=(8, 8))
    plt.pie(top_10_city_prices, labels=top_10_city_prices.index, autopct='%1.1f%%', startangle=140)
    plt.title("Average Price Distribution by City (Top 10 Cities with Others)")
    plt.show()

def create_heatmap():
    # Calculating the correlation matrix for the numerical columns in the cleaned dataset
    correlation_matrix = cleaned_housing_data.select_dtypes(include=[np.number]).corr()

    # Plotting a heatmap to visualize the correlations
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", cbar=True, fmt=".2f")
    plt.title("Correlation Heatmap of Houston Housing Market Data")
    plt.show()


cleaned_housing_data = clean_up_data()
# create_scatter_plots()
# create_bar_plots()
# create_box_plot()
# create_box_plot_no_outliers()
# create_pie_charts()
create_heatmap()