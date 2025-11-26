import os
import django
import pandas as pd
from pathlib import Path

# configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netflixsite.settings")
django.setup()

# import model after setting up Django to insert / update data
from dashboard.models import NetflixTitle

# CSV path to cleaned data 
csv_path = Path(__file__).resolve().parent.parent / "data" / "cleaned_netflix_titles.csv"

# Loading cleaned CSV
df = pd.read_csv(csv_path)

# Convert 'date_added' to proper datetime, handle missing values 
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')  # NaT if missing or incorrect format (need this for formatting) 

# Populate database
for _, row in df.iterrows():# loop through each row in the dataframe
    NetflixTitle.objects.update_or_create( # prevents duplicates based on show_id
        show_id=row['show_id'], # unique identifier for each show
        defaults={
            'title': row['title'],
            'type': row['type'],
            'director': row['director'],
            'cast': row['cast'],
            'country': row['country'],
            'release_year': row['release_year'],
            'rating': row['rating'],
            'duration': row['duration'],
            'description': row['description'],
            'date_added': row['date_added'].date() if pd.notnull(row['date_added']) else None,
            #convert to datetime to date only, if not a time 
            'listed_in': row['listed_in']
        }
    )
#confirmation message ( helps confirm script ran successfully)
print("Database load complete!")

