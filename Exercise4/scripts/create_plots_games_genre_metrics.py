import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Get the absolute directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the data folder
file_path = os.path.join(script_dir, "../data", "games_genre_metrics.csv")

# Read the CSV file
games_genre_metrics = pd.read_csv(file_path)

# Bar chart for total revenue by genre
def create_bar_charts():

    # Bar Chart 1: Average Playtime Forever by Genre
    plt.figure(figsize=(10,6))
    plt.bar(games_genre_metrics['Genres'], games_genre_metrics['Average_Playtime_Forever'], color='purple')
    plt.title('Average Playtime Forever by Genre')
    plt.xlabel('Genres')
    plt.ylabel('Average Playtime (hours)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    # Bar Chart 2: Total Revenue by Genre: Top 16 genres
    # Sort the data by total revenue and select the top 16 genres
    top_16_genres = games_genre_metrics.sort_values(by='Total_Revenue', ascending=False).head(16)

    plt.figure(figsize=(10,6))
    plt.bar(top_16_genres['Genres'], top_16_genres['Total_Revenue'], color='orange')
    plt.title('Top 16 Genres by Total Revenue')
    plt.xlabel('Genres')
    plt.ylabel('Total Revenue ($)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    # Bar Chart 3: Revenue Per Game by Genre
    # Calculate the revenue per game for each genre
    games_genre_metrics['Revenue_Per_Game'] = games_genre_metrics['Total_Revenue'] / games_genre_metrics['Number_of_Games']

    plt.figure(figsize=(10,6))
    plt.bar(games_genre_metrics['Genres'], games_genre_metrics['Revenue_Per_Game'], color='blue')
    plt.title('Revenue Per Game by Genre')
    plt.xlabel('Genres')
    plt.ylabel('Revenue Per Game ($)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# Group genres that contribute less than 2% into an "Other" category for pie charts
def group_small_values(data, values_col, labels_col, threshold=0.02):
    # Create a copy of the input data to avoid modifying the original dataframe.
    data = data.copy()
    total = data[values_col].sum()

    # Calculate the percentage of each row, by adding a new column called Percentage
    data['Percentage'] = data[values_col] / total
    large_values = data[data['Percentage'] >= threshold]

    # Sum up the values from the rows that contribute less than the threshold
    small_values_sum = data[data['Percentage'] < threshold][values_col].sum()

    # Combine the large values (keep as they are), and the "Other" category
    grouped_data = pd.concat([large_values, pd.DataFrame([{labels_col: 'Other', values_col: small_values_sum}])], ignore_index=True)
    
    return grouped_data

def create_pie_charts(games_genre_metrics):
    # Group genres for each pie chart (Total Revenue, Total Estimated Players, Number of Games)
    grouped_revenue = group_small_values(games_genre_metrics, 'Total_Revenue', 'Genres')
    grouped_players = group_small_values(games_genre_metrics, 'Total_Estimated_Players', 'Genres')
    grouped_games = group_small_values(games_genre_metrics, 'Number_of_Games', 'Genres')

    # Pie Chart 1: Grouped Revenue Share by Genre
    plt.figure(figsize=(8,8))
    plt.pie(grouped_revenue['Total_Revenue'], labels=grouped_revenue['Genres'], autopct='%1.1f%%', startangle=140)
    plt.title('Grouped Revenue Share by Genre')
    plt.tight_layout()
    plt.show()

    # Pie Chart 2: Grouped Proportion of Total Estimated Players by Genre
    plt.figure(figsize=(8,8))
    plt.pie(grouped_players['Total_Estimated_Players'], labels=grouped_players['Genres'], autopct='%1.1f%%', startangle=140)
    plt.title('Grouped Proportion of Total Estimated Players by Genre')
    plt.tight_layout()
    plt.show()

    # Pie Chart 3: Grouped Number of Games Share by Genre
    plt.figure(figsize=(8,8))
    plt.pie(grouped_games['Number_of_Games'], labels=grouped_games['Genres'], autopct='%1.1f%%', startangle=140)
    plt.title('Grouped Number of Games Share by Genre')
    plt.tight_layout()
    plt.show()


def create_scatterplots():
    # Scatter Plot 1: Average Playtime vs. Number of Games by Genre
    plt.figure(figsize=(10,6))
    plt.scatter(games_genre_metrics['Number_of_Games'], games_genre_metrics['Average_Playtime_Forever'], color='green')
    plt.title('Average Playtime vs. Number of Games by Genre')
    plt.xlabel('Number of Games')
    plt.ylabel('Average Playtime (hours)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Scatter Plot 2: Average Positive Review Rate vs. Average Playtime by Genre
    plt.figure(figsize=(10,6))
    plt.scatter(games_genre_metrics['Average_Playtime_Forever'], games_genre_metrics['Average_Positive_Review_Rate'], color='blue')
    plt.title('Average Positive Review Rate vs. Average Playtime by Genre')
    plt.xlabel('Average Playtime (hours)')
    plt.ylabel('Average Positive Review Rate')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Scatter Plot 3: Total Estimated Players vs Total Revenue by Genre
    plt.figure(figsize=(10,6))
    plt.scatter(games_genre_metrics['Total_Estimated_Players'], games_genre_metrics['Total_Revenue'], color='blue')
    plt.title('Total Estimated Players vs. Total Revenue by Genre')
    plt.xlabel('Total Estimated Players')
    plt.ylabel('Total Revenue ($)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def create_heatmap_correlation():
    # Exclude non-numeric columns before calculating the correlation matrix
    numeric_data = games_genre_metrics.select_dtypes(include=[np.number])  # assuming you have numpy imported as np

    # Calculate the correlation matrix
    correlation_matrix = numeric_data.corr()

    # Heatmap of the correlation matrix
    plt.figure(figsize=(12, 10))  # Adjust the figure size as needed
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", cbar_kws={'shrink': .8})
    plt.title('Correlation Heatmap of Gaming Metrics')
    plt.xticks(rotation=45)  # Rotate x labels for better visibility
    plt.yticks(rotation=0)   # Ensure y labels are horizontal for clarity
    plt.tight_layout()       # This adjusts subplots to give some padding and prevent cutoff
    plt.show()

# Show the first few rows to understand the structure of the data
print(games_genre_metrics.head())
create_pie_charts(games_genre_metrics)
create_scatterplots()
create_bar_charts()
create_heatmap_correlation()