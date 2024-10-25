# Project 5 - Exercise 3: MongoDB Collections

## Overview
This part of the project focuses on inserting anime datasets into a MongoDB database and creating views for filtering and aggregating the data. The datasets are sourced from MyAnimeList, and the insertion and view creation are performed using a Python script.

### Prerequisites

1. To run this project, ensure you have the following installed:
- **Python 3.8+**
- **MongoDB** 
- **pip** (the Python package installer)

2. To be able to run the python script, install the required libraries by running:

 ```bash
    pip install -r requirements.txt
```

3. After cloning the repository, download the large data files directly from the [Kaggle dataset website](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset/data?select=users-details-2023.csv) into the data folder!!!

### MongoDB Setup

1. **Install MongoDB**:
   If MongoDB is not installed on your system, you can download and install it from the official MongoDB website:
   - [MongoDB Download](https://www.mongodb.com/try/download/community)

2. **Start the MongoDB Server**:

   Open a terminal or command prompt and run the following command to start the MongoDB server:
    ```bash
     mongod
     ```
     or
     ```bash
     mongod --dbpath <path-to-mongod-installation>
     ```
   The server will run on `localhost:27017` by default. Ensure it stays running while you're interacting with the database.

3. **Access the MongoDB Shell**:

   To manually interact with the MongoDB database (to see the collections, views and indices cerated), open a new terminal window and use the MongoDB shell by typing:
   ```bash
   mongosh
   ```

4. **Create the Database by Running the Script**
    ```bash
   python scripts/mongodb_insert_script.py
   ```

    This script will:

    - Insert CSV files into corresponding MongoDB collections.
    - Create 6 views in which filtering is performed. 
    - Create 6 views in which aggregation is performed.
    - Create 6 indexes on different collections to optimize queries.

5. **Query the Database**

    Useful MongoDB Commands to run in the mongosh console:
- Show all databases: `show dbs`
- Switch to the `anime_db` database: `use anime_db`
- Show all collections in the current database: `show collections`
- Show the first 5 documents in a view:
 `db.<insert_view_name>.find().limit(5).pretty()`
- Show all indexes on a collection: `db.<insert_collection_name>.getIndexes()`

