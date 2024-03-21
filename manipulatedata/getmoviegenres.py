import pandas as pd
import json


filepath = "./tmdb_5000_movies.csv"

movies_df = pd.read_csv(filepath)

# Initializing a list to hold the movie-genre relationships
movie_genre_relations = []

# Iterating over the dataframe to extract movie ID and associated genre IDs
for index, row in movies_df.iterrows():
    movie_id = row['id']
    genres = json.loads(row['genres'])
    for genre in genres:
        movie_genre_relations.append((movie_id, genre['id']))

# Creating a dataframe for the movie-genre relationship
movie_genre_df = pd.DataFrame(movie_genre_relations, columns=['movie_id', 'genre_id'])

# Saving the dataframe to a new CSV file
movie_genre_output_path = './movie_genre_relationships.csv'
movie_genre_df.to_csv(movie_genre_output_path, index=False)

movie_genre_output_path, movie_genre_df.head()