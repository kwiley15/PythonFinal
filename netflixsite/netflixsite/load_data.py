import pandas as pd
from .models import NetflixTitle

df = pd.read_csv("../data/netflix_titles.csv")
for _, row in df.iterrows():
    NetflixTitle.objects.create(
        show_id=row['show_id'],
        title=row['title'],
        type=row['type'],
        director=row['director'],
        country=row['country'],
        release_year=row['release_year'],
        rating=row['rating'],
        date_added=row['date_added'],
        listed_in=row['listed_in']
    )
