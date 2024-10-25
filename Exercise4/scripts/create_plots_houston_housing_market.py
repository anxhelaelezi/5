import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

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


cleaned_housing_data = clean_up_data()
create_scatter_plots()
create_bar_plots()