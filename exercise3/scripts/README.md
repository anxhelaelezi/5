## Reasoning Behind The Choice of Views and Indices

## Overview
This project processes large datasets of anime and user details from MyAnimeList using MongoDB. Several **filtering** and **aggregation views** have been created to answer common user queries and perform analysis. Additionally, **indices** have been applied to optimize query performance, one for each collection.

### Views

#### Filtering Views
1. **Currently Airing Anime**
   - **Purpose**: Retrieve all anime that are still being broadcast.
   - **Reasoning**: Ongoing anime is a frequent user interest, and having a view that quickly filters by `Status` ("Currently Airing") optimizes this common request.
   
2. **Sci-Fi Genre Anime**
   - **Purpose**: Retrieve all anime belonging to the "Sci-Fi" genre.
   - **Reasoning**: Genre-based queries are common, and filtering by `Genres` allows users to explore specific categories like Sci-Fi. A genre filter allows for better user discovery.

3. **Long Running Anime (More than 50 episodes)**
   - **Purpose**: Retrieve anime with more than 50 `episodes`.
   - **Reasoning**: Long-running anime tends to have a dedicated audience. This view helps find anime with substantial episode counts by filtering and converting episode numbers stored as strings into double types.

4. **Users Who Completed More Than 500 Anime**
   - **Purpose**: Identify users who have completed over 500 anime (often high-engagement users or bots).
   - **Reasoning**: Analyzing users with extreme viewing patterns can be valuable for targeting highly active users or detecting potential bots. This view quickly filters users based on the `Completed` field.

5. **Popular Anime by Favourites**
   - **Purpose**: Retrieve anime with more than 100,000 favorites, sorted by number of favorites.
   - **Reasoning**: Anime popularity, measured by user `Favourites`, is a key metric for identifying community engagement. This view highlights anime that are particularly popular among the user base.

6. **Top-Rated Anime (Score > 9)**
   - **Purpose**: Retrieve anime with a score greater than 9.
   - **Reasoning**: Users often search for highly-rated anime. This view filters by `Score` to quickly return top-rated anime, ensuring that users can easily find critically acclaimed shows. Score is converted to a double type from a string type.

#### Aggregation Views
1. **Average Score of Anime by Genre**
   - **Purpose**: Calculate the average score for each genre.
   - **Reasoning**: This aggregation helps users and analysts understand which genres tend to be rated higher by the community. The `Genres` field is split, and the average score is calculated per genre.

2. **Number of Anime per Genre**
   - **Purpose**: Count the number of anime for each genre.
   - **Reasoning**: This provides insight into genre distribution within the anime dataset, allowing for analysis of content availability across genres.

3. **Average Score per Studio**
   - **Purpose**: Calculate the average score for each studio.
   - **Reasoning**: Studios known for producing high-quality anime can be identified by this view, which groups by `Studios` and computes the average score.

4. **Top 10 Countries by Number of Users**
   - **Purpose**: Identify the top 10 countries with the most users.
   - **Reasoning**: Understanding user distribution by country is crucial for localization and marketing strategies. This view groups users by `Location` and counts the number of users in each country.

5. **Most Active Users by Total Episodes Watched**
   - **Purpose**: Identify the most active users based on total episodes watched.
   - **Reasoning**: Highly engaged users can be valuable for targeted campaigns and rewards. This view sums the total number of episodes watched for each user.

6. **Top Producers by Anime Count**
   - **Purpose**: Identify the most prolific anime producers by counting the number of anime produced by each producer.
   - **Reasoning**: Understanding which producers dominate the anime industry is valuable for industry analysis and partnerships.

---

### Indices

To optimize query performance, specific fields that are frequently queried or filtered were indexed.

1. **`anime_dataset_2023`**
   - **Index**: `{ "Genres": 1, "Score": -1, "Favourites": -1 }`
   - **Reasoning**: This dataset is queried frequently by `Genres` (for filtering by genre), `Score` (for sorting by ratings), and `Favourites` (for identifying popular anime). Indexing these fields improves the performance of views related to anime filtering and ranking.

2. **`anime_filtered`**
   - **Index**: `{ "Genres": 1, "Episodes": 1 }`
   - **Reasoning**: Filtering by `Genres` and sorting by `Episodes` allows for faster queries when identifying long-running anime and genre-specific searches.

3. **`final_animedataset`**
   - **Index**: `{ "Genres": 1 }`
   - **Reasoning**: This dataset is used in aggregations and filtering based on `Genres`. Indexing the `Genres` field improves performance for genre-based queries, such as finding the number of anime per genre.

4. **`user_filtered`**
   - **Index**: `{ "Completed": 1 }`
   - **Reasoning**: Queries that focus on the number of anime users have completed are common for identifying highly active users. Indexing `Completed` ensures that these queries perform efficiently.

5. **`users_details_2023`**
   - **Index**: `{ "Location": 1, "Episodes Watched": -1 }`
   - **Reasoning**: This dataset is indexed by `Location` (for geographic distribution of users) and `Episodes Watched` (for sorting users by activity). This improves the performance of views that rank user activity or analyze users by country.

6. **`users_score_2023`**
   - **Index**: `{ "anime_id": 1, "score": -1 }`
   - **Reasoning**: This dataset contains user ratings of anime. Indexing `anime_id` and `score` improves the performance of queries related to finding anime ratings by users and sorting them by score.

---

### Conclusion
The filtering and aggregation views were designed to answer common user queries and provide insightful analysis on anime data, such as identifying popular anime, active users, and highly-rated genres. The indices were carefully chosen to optimize performance for frequently queried fields, ensuring the database can handle large datasets efficiently.
