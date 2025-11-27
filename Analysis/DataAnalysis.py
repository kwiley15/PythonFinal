import pandas as pd
from pathlib import Path


#Load data 
DATA = Path("Data/netflix_titles.csv") 
OUTPUT_CSV = Path("Data/cleaned_netflix_titles.csv")
PLOTS_DIR = Path(__file__).resolve().parent.parent / "netflixsite" / "dashboard" / "static" / "dashboard" / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

#load raw data
df = pd.read_csv(DATA)
print("data loaded successfully")


#Data Cleaning
#convert date into datetime 
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

#handel missing date values by filling with the mode / most common year
df['release_year'] = df['release_year'].fillna(df['release_year'].mode()[0])

#fill in missing values was not sure what to do here so we just filled with 'Unknown'
for col in ['director', 'cast', 'country', 'rating']:
    df[col] = df[col].fillna('Unknown')

#extract year from date_added
df['year_added'] = df['date_added'].dt.year

#save cleaned data
df.to_csv(OUTPUT_CSV, index=False)
print(f"cleaned data saved to {OUTPUT_CSV}")














