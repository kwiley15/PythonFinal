import pandas as pd
from pathlib import Path


#Load data 
DATA = Path("Data/netflix_titles.csv") 
df = pd.read_csv(DATA)


#print data 
print("data loaded successfully")
print(df.head())

print(df.info())

print("missing values per column")
print(df.isnull().sum())
















