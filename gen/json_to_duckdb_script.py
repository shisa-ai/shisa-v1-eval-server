
import pandas as pd
import json
import os

# Load the JSON file
file_path = '/path/to/your/file.json'  # Change this to your actual file path
with open(file_path, 'r') as file:
    data = json.load(file)

# Extracting the filename info
filename = os.path.basename(file_path)
model, temp, run = filename.replace('.json', '').split('_')

# Creating dataframes
models_df = pd.DataFrame([{'model': model, 'temp': temp, 'run': run}])

# Creating tasks dataframe
tasks = []
for item in data:
    task = item['task']
    tasks.append(task)

tasks_df = pd.DataFrame(tasks).drop_duplicates(subset=['id'])

# Creating generations dataframe
generations = []
for item in data:
    task_id = item['task']['id']
    generation_data = {
        'chat': item['chat'],
        'response': item['response'],
        'lang': item['lang'],
        'run': run,
        'task_id': task_id
    }
    generations.append(generation_data)

generations_df = pd.DataFrame(generations)

# Example of how to use the dataframes
print(models_df.head())
print(tasks_df.head())
print(generations_df.head())
