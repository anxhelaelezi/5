import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Get the absolute directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the data folder
file_path = os.path.join(script_dir, "../data", "games_yearly_revenue.csv")

# Read the CSV file
games_yearly_revenue = pd.read_csv(file_path)

def create_line_plots():
    # Line Plot 1: Yearly trend of total estimated revenue over time
    plt.figure(figsize=(14, 5))
    sns.lineplot(x='Release_Year', y='Total_Estimated_Revenue', data=games_yearly_revenue, marker='o')
    plt.title('Yearly Trend of Total Estimated Revenue')
    plt.xlabel('Release Year')
    plt.ylabel('Total Estimated Revenue')
    plt.show()

    # Line Plot 2: Yearly trend of total estimated owners over time
    plt.figure(figsize=(14, 5))
    sns.lineplot(x='Release_Year', y='Total_Estimated_Owners', data=games_yearly_revenue, marker='o')
    plt.title('Yearly Trend of Total Estimated Owners')
    plt.xlabel('Release Year')
    plt.ylabel('Total Estimated Owners')
    plt.show()

    # Line Plot 3: Yearly trend of the number of games released
    plt.figure(figsize=(14, 5))
    sns.lineplot(x='Release_Year', y='Number_of_Games', data=games_yearly_revenue, marker='o')
    plt.title('Yearly Trend of Number of Games Released')
    plt.xlabel('Release Year')
    plt.ylabel('Number of Games')
    plt.show()

def create_bar_plots():
    # Bar chart for Total Estimated Revenue by Year
    plt.figure(figsize=(10, 5))
    plt.bar(games_yearly_revenue['Release_Year'], games_yearly_revenue['Total_Estimated_Revenue'], color='blue')
    plt.title('Total Estimated Revenue by Release Year')
    plt.xlabel('Release Year')
    plt.ylabel('Total Estimated Revenue')
    plt.show()

    # Bar chart for Total Estimated Owners by Year
    plt.figure(figsize=(10, 5))
    plt.bar(games_yearly_revenue['Release_Year'], games_yearly_revenue['Total_Estimated_Owners'], color='green')
    plt.title('Total Estimated Owners by Release Year')
    plt.xlabel('Release Year')
    plt.ylabel('Total Estimated Owners')
    plt.show()

    # Bar chart for Number of Games by Year
    plt.figure(figsize=(10, 5))
    plt.bar(games_yearly_revenue['Release_Year'], games_yearly_revenue['Number_of_Games'], color='red')
    plt.title('Number of Games by Release Year')
    plt.xlabel('Release Year')
    plt.ylabel('Number of Games')
    plt.show()


create_line_plots()