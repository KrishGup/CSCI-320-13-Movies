import pandas as pd
import json
from itertools import count


filepath = "./tmdb_5000_credits.csv"

credits_df = pd.read_csv(filepath)

# Initializing a set to hold the unique names
unique_names = set()

# Function to extract names from JSON-formatted text
def extract_names(json_text):
    items = json.loads(json_text)
    for item in items:
        unique_names.add(item['name'])

# Extracting names from both cast and crew columns
credits_df['cast'].apply(extract_names)
credits_df['crew'].apply(extract_names)

# Assigning a unique ID to each name (using enumeration for simplicity)
contributor_ids = range(1, len(unique_names) + 1)
contributor_data = zip(contributor_ids, unique_names)

# Creating a dataframe for the contributors
contributor_df = pd.DataFrame(contributor_data, columns=['contributor_id', 'name'])

# Saving the dataframe to a new CSV file
contributor_output_path = './contributors.csv'
contributor_df.to_csv(contributor_output_path, index=False)

contributor_output_path, contributor_df.head()