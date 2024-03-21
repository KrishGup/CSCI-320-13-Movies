import pandas as pd
import json

credits = "./tmdb_5000_credits.csv"

credits_df = pd.read_csv(credits)
contributor_df = pd.read_csv("./contributors.csv")

# Function to extract all roles (actors and crew) and their movie IDs from the cast and crew data
def extract_roles(movie_id, cast_json, crew_json):
    roles = []
    # Actors
    cast = json.loads(cast_json)
    for member in cast:
        roles.append((movie_id, member['name'], 'Actor'))
    # Crew
    crew = json.loads(crew_json)
    for member in crew:
        roles.append((movie_id, member['name'], member['job']))
    return roles

# Applying the function to each row in the credits DataFrame
roles_movie_pairs = credits_df.apply(lambda x: extract_roles(x['movie_id'], x['cast'], x['crew']), axis=1)

# Flattening the list of lists
roles_movie_flat = [item for sublist in roles_movie_pairs for item in sublist]

# Creating a DataFrame for roles and their movie IDs
roles_movie_df = pd.DataFrame(roles_movie_flat, columns=['movie_id', 'name', 'job'])

# Merging with the contributors table to get the contributor IDs for each person
produce_df = pd.merge(roles_movie_df, contributor_df, how='left', on='name')

# Selecting only the necessary columns
produce_df_final = produce_df[['contributor_id', 'movie_id', 'job']]

# Saving the DataFrame to a new CSV file
produce_output_path = './produce.csv'
produce_df_final.to_csv(produce_output_path, index=False)

produce_output_path, produce_df_final.head()
