import pandas as pd

# Assuming the filepath is correct and pandas can access the file directly
filepath = "tmdb_5000_movies.csv"

movies_df = pd.read_csv(filepath)

# Preparing a list to hold the (movie_id, release_date, host_id) tuples
host_relation = []

# Iterating through each row in the movies DataFrame
for index, row in movies_df.iterrows():
    movie_id = row['id']
    release_date = row['release_date']
    host_id = 42  # This will be a constant value
    host_relation.append((movie_id, release_date, host_id))

# Creating a new DataFrame from the list
host_df = pd.DataFrame(host_relation, columns=['movie_id', 'release_date', 'host_id'])

# Saving the new DataFrame to a CSV file
output_path = 'hosts.csv'
host_df.to_csv(output_path, index=False)