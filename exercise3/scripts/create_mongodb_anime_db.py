import os
from tqdm import tqdm
import pymongo
import pandas as pd

# Get the directory containing the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the data folder
data_dir = os.path.join(script_dir, "../data")

# Establish a connection to MongoDB and the anime_db database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["anime_db"]

# Function to insert data from CSV to MongoDB collection
def insert_csv_to_collection(file_name, collection_name):
    # Construct the full path to the file by combining the script's directory and the file name
    file_path = os.path.join(data_dir, file_name)
    print(f"Processing file at: {file_path}")
    
    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(file_path)
    
    # Convert the DataFrame to a dictionary format that MongoDB accepts
    data_dict = data.to_dict("records")
    
    # Insert the data into the MongoDB collection
    collection = db[collection_name]
    collection.insert_many(data_dict)
    print(f"Data inserted into collection '{collection_name}' successfully!")

# Function to insert data into MongoDB in chunks for larger datasets
def insert_csv_in_chunks(file_name, collection_name, chunk_size=10000):
    file_path = os.path.join(script_dir, file_name)
    print(f"Processing file at: {file_path}")

    # Create the MongoDB collection
    collection = db[collection_name]

    # Read the CSV file in chunks, using tqdm library to print the progress
    total_rows = sum(1 for _ in open(file_path))
    for chunk in tqdm(pd.read_csv(file_path, chunksize=chunk_size), total=(total_rows // chunk_size) + 1, desc=f"Inserting {collection_name}"):
        # Convert the chunk to a list of dictionaries (records) and insert into MongoDB
        data_dict = chunk.to_dict(orient="records")
        collection.insert_many(data_dict)
    
    print(f"Data inserted into collection '{collection_name}' successfully!")

def insert_datasets():
    # Insert the datasets into MongoDB collections using filenames relative to the script directory
    insert_csv_to_collection("anime-dataset-2023.csv", "anime_dataset_2023")
    insert_csv_to_collection("users-details-2023.csv", "users_details_2023")
    insert_csv_to_collection("anime-filtered.csv", "anime_filtered")

    # Insert the large dataset in chunks because it is a huge dataset
    insert_csv_in_chunks("final_animedataset.csv", "final_animedataset")
    insert_csv_in_chunks("user-filtered.csv", "user_filtered")
    insert_csv_in_chunks("users-score-2023.csv", "users_score_2023")

# Function to create a view
def create_view(view_name, source_collection, pipeline):
    try:
        db.command({
            "create": view_name,
            "viewOn": source_collection,
            "pipeline": pipeline
        })
        print(f"View '{view_name}' created successfully.")
    except pymongo.errors.PyMongoError as e:
        print(f"Error creating view '{view_name}': {str(e)}")

# Function to create an index on a collection
def create_index(collection_name, index_fields, index_name):
    try:
        db[collection_name].create_index(index_fields, name=index_name)
        print(f"Index '{index_name}' created successfully on '{collection_name}'.")
    except pymongo.errors.PyMongoError as e:
        print(f"Error creating index '{index_name}': {str(e)}")

def create_filtering_views():
    # 1. Filter anime with status currently airing
    create_view(
        "currently_airing_anime",
        "anime_dataset_2023",
        [{ "$match": { "Status": "Currently Airing" } }]
    )

    # 2. Filter anime that belong to the "Sci-Fi" genre
    create_view(
        "sci_fi_genre_anime",
        "anime_dataset_2023",
        [{ "$match": { "Genres": "Sci-Fi" } }]
    )

    # 3. Filter anime with more than 50 episodes
    create_view(
        view_name="long_running_anime",
        source_collection="anime_dataset_2023",
        pipeline=[
            { 
                "$match": { 
                    "Episodes": { "$regex": "^[0-9]+\\.?[0-9]*$" }  # Filter out non-floats
                }
            },
            { 
                "$match": { 
                    "$expr": { 
                        "$gt": [ { "$toDouble": "$Episodes" }, 50 ]  # Convert Episodes to float and filter for > 50
                    }
                }
            }
        ]
    )

    # 4. Filter users who have completed more than 500 anime -> likely bots
    create_view(
        "users_watched_more_than_500",
        "users_details_2023",
        [
            { "$match": { "Completed": { "$gt": 500 } } }
        ]
    )

    # 5. Anime with more than 100000 favourites
    create_view(
        view_name="popular_anime_by_favourites",
        source_collection="anime_dataset_2023",
        pipeline=[
            { 
                "$match": { 
                    "Favorites": { "$gt": 100000 }
                }
            },
            { "$sort": { "Favorites": -1 } }
        ]
    )

    # 6. Top rate anime with a score greater than 9
    create_view(
    view_name="top_rated_anime",
    source_collection="anime_dataset_2023",
    pipeline=[
        { 
            "$match": { 
                "Score": { "$regex": "^[0-9]+\\.?[0-9]*$" }  # Only allow numeric score values (with optional decimals)
            }
        },
        { 
            "$match": { 
                "$expr": { 
                    "$gt": [ { "$toDouble": "$Score" },  9  ] 
                } 
            }
        }
    ]
)

def create_aggregation_views():
    # 1. Average score of anime by genre
    create_view(
        view_name="avg_score_by_genre",
        source_collection="anime_dataset_2023",
        pipeline=[
            { 
                "$set": { 
                    "GenresArray": { "$split": ["$Genres", ", "] }  # Split the genres string into an array
                }
            },
            { 
                "$unwind": "$GenresArray"  # Unwind the genres array to process each genre individually
            },
            { 
                "$match": { 
                    "Score": { "$regex": "^[0-9]+\\.?[0-9]*$" }  # Filter out non-numeric scores
                }
            },
            { 
                "$group": {
                    "_id": "$GenresArray",  # Group by individual genres
                    "avg_score": { 
                        "$avg": { 
                            "$toDouble": "$Score"  # Convert Score to a number and calculate the average
                        } 
                    }
                }
            },
            { "$sort": { "avg_score": -1 } } 
        ]
    )

    # 2. Number of anime per genre
    create_view(
        view_name="num_anime_per_genre",
        source_collection="final_animedataset",
        pipeline=[
            { 
                "$set": { 
                    "GenresArray": { "$split": ["$Genres", ", "] }  # Split the genres string into an array
                }
            },
            { 
                "$unwind": "$GenresArray"  # Unwind the genres array to process each genre individually
            },
            { "$group": {
                "_id": "$GenresArray",
                "num_anime": { "$sum": 1 }  # Count number of anime in each genre
            }},
            { "$sort": { "num_anime": -1 } }
        ]
    )

    # 3. Average score per studio
    create_view(
        view_name="top_studios_by_avg_score",
        source_collection="anime_dataset_2023",
        pipeline=[
            { 
                "$match": { 
                    "Score": { "$regex": "^[0-9]+\\.?[0-9]*$" }  # Ensure score is numeric
                }
            },
            { 
                "$group": {
                    "_id": "$Studios",  # Group by studio name
                    "avg_score": { 
                        "$avg": { "$toDouble": "$Score" }  # Calculate average score after converting score to double
                    }
                }
            },
            { "$sort": { "avg_score": -1 } },  # Sort by average score in descending order
            { "$limit": 10 }  # Get the top 10 studios
        ]
    )

    # 4. Top 10 coutnries with most users
    create_view(
        view_name="country_with_most_users",
        source_collection="users_details_2023",
        pipeline=[
            { 
                "$match": { 
                    "Location": { "$exists": True, "$ne": None, "$ne": "" }  # Exclude documents with null or empty locations
                }
            },
            { 
                "$group": {
                    "_id": "$Location",  # Group by the Location field (assumed to be country)
                    "user_count": { "$sum": 1 }  # Count the number of users in each location
                }
            },
            { "$sort": { "user_count": -1 } },  # Sort by user count in descending order
            { "$limit": 10 }  # Limit to the country with the most users
        ]
    )


    # 5. Most active users by total episodes watched
    create_view(
        view_name="most_active_users_by_total_episodes_watched",
        source_collection="users_details_2023",
        pipeline=[
            { 
                "$group": {
                    "_id": "$Username",  # Group by Username instead of Mal ID
                    "total_episodes_watched": { "$sum": "$Episodes Watched" }  # Sum the total episodes watched by each user
                }
            },
            { "$sort": { "total_episodes_watched": -1 } },  # Sort by total episodes watched in descending order
            { "$limit": 10 }  # Limit to the top 10 most active users
        ]
    )

    # 6. Top producers by anime count
    create_view(
        view_name="top_producers_by_anime_count",
        source_collection="anime_dataset_2023",
        pipeline=[
            { 
                "$set": { 
                    "ProducersArray": { "$split": ["$Producers", ", "] }  # Split the producers string into an array
                }
            },
            { 
                "$unwind": "$ProducersArray"  # Unwind the producers array to process each producer individually
            },
            { 
                "$group": {
                    "_id": "$ProducersArray",  # Group by individual producers
                    "anime_count": { "$sum": 1 }  # Count the number of anime produced by each producer
                }
            },
            { "$sort": { "anime_count": -1 } },  # Sort by anime count in descending order
            { "$limit": 10 }  # Limit to the top 10 producers
        ]
    )

def create_indices():
    # 1. Index for anime-dataset-2023.csv
    create_index(
        collection_name="anime_dataset_2023",
        # Composite index on Status, Genres, and Score
        index_fields=[("Genres", pymongo.ASCENDING), ("Score", pymongo.DESCENDING), ("Favourites", pymongo.DESCENDING)],
        index_name="status_genres_score_index"
    )

    # 2. Index for anime-filtered.csv
    create_index(
        collection_name="anime_filtered",
        # Composite index on Genres and Episodes
        index_fields=[("Genres", pymongo.ASCENDING), ("Episodes", pymongo.ASCENDING)],
        index_name="genres_episodes_index"
    )

    # 3. Index for final-animedataset.csv
    create_index(
        collection_name="final_animedataset",
        index_fields=[("Genres", pymongo.ASCENDING)],
        index_name="genres_index"
    )

    # 4. Index for user-filtered.csv
    create_index(
        collection_name="user_filtered",
        index_fields=[("Completed", pymongo.ASCENDING)],
        index_name="completed_index"
    )

    # 5. Index for users-details-2023.csv
    create_index(
        collection_name="users_details_2023",
        index_fields=[("Location", pymongo.ASCENDING), ("Episodes Watched", pymongo.DESCENDING)],
        index_name="location_episodes_watched_index"
    )

    # 6. Index for users-score-2023.csv
    create_index(
        collection_name="users_score_2023",
        index_fields=[("anime_id", pymongo.ASCENDING), ("score", pymongo.DESCENDING)],
        index_name="user_anime_score_index"
    )

# Create the datatsets, views and indices
# To disable any of the following calls, comment out the line
insert_datasets()
create_filtering_views()
create_aggregation_views()
create_indices()
