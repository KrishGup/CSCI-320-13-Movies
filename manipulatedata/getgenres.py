import pandas as pd
import json


filepath = "./tmdb_5000_movies.csv"

movies_df = pd.read_csv(filepath)

# Extracting genres and their IDs
genre_list = []

# Iterating over the genres column to parse the JSON content
for genre_json in movies_df['genres']:
    genres = json.loads(genre_json)
    for genre in genres:
        genre_list.append((genre['id'], genre['name']))

# Creating a dataframe of unique genre-genre_id pairs
genre_df = pd.DataFrame(set(genre_list), columns=['gid', 'genrename'])

# Saving the dataframe to a new CSV file
output_path = './unique_genres.csv'
genre_df.to_csv(output_path, index=False)

output_path, genre_df.head()