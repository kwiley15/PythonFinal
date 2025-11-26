import os
import django
import pandas as pd
from pathlib import Path

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netflixsite.settings")
django.setup()

from dashboard.models import NetflixTitle

# CSV path
csv_path = Path(__file__).resolve().parent.parent / "data" / "cleaned_netflix_titles.csv"

# Load CSV
df = pd.read_csv(csv_path)

# Convert 'date_added' to proper datetime, handle missing values
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')  # NaT if missing

# Populate database
for _, row in df.iterrows():
    NetflixTitle.objects.update_or_create(
        show_id=row['show_id'],
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
            'listed_in': row['listed_in']
        }
    )

print("Database load complete!")

