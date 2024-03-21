import pandas as pd
import json

credits = "./tmdb_5000_credits.csv"

credits_df = pd.read_csv(credits)
contributor_df = pd.read_csv("./contributors.csv")


# Mapping names to contributor IDs for easy lookup
name_to_contributor_id = {row['name']: row['contributor_id'] for index, row in contributor_df.iterrows()}

# Initializing a list to hold the director-movie relationships
director_movie_relations = []

# Function to extract director names and their movie ID
def extract_director_movie_relations(row):
    movie_id = row['movie_id']
    crew = json.loads(row['crew'])
    for member in crew:
        if member['job'].lower() == 'director' and member['name'] in name_to_contributor_id:
            director_id = name_to_contributor_id[member['name']]
            director_movie_relations.append((director_id, movie_id))

# Applying the function to each row in the credits dataframe
credits_df.apply(extract_director_movie_relations, axis=1)

# Creating a dataframe for the directs table
directs_df = pd.DataFrame(director_movie_relations, columns=['contributor_id', 'movie_id'])

# Saving the dataframe to a new CSV file
directs_output_path = './directs.csv'
directs_df.to_csv(directs_output_path, index=False)

directs_output_path, directs_df.head()
