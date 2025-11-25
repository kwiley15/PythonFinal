import pandas as pd
from pathlib import Path


#Load data 
DATA = Path("Data/netflix_titles.csv") 
df = pd.read_csv(DATA)
print("data loaded successfully")


#Data Cleaning
#convert date into datetime 
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

#handel missing date values by filling with the mode 
df['release_year'] = df['release_year'].fillna(df['release_year'].mode()[0])

#fill in missing values was not sure what to do here so we just filled with 'Unknown'
for col in ['director', 'cast', 'country', 'rating']:
    df[col] = df[col].fillna('Unknown')

#extract year from date_added
df['year_added'] = df['date_added'].dt.year

print("data cleaned successfully")
print(df.info())

print("missing values per column")
print(df.isnull().sum())














