import matplotlib.pyplot as plt
from DataAnalysis import df, PLOTS_DIR

#the 5 visualizations we need (only need 3 but extra marks (5th one looks weird ) )

#most common genres
grene_count = df['listed_in'].str.split(',').explode().str.strip().value_counts().head(10)
plt.figure()
grene_count.plot(kind='bar')
plt.title('Top 10 Most Common Genres on Netflix')
plt.xlabel('Genre')
plt.ylabel('Nummber of Titles') 
plt.xticks(rotation=25)
plt.savefig(PLOTS_DIR/ "Most_Common_Genres.png")
plt.show() 


#content distribution by rating

rating_count = df['rating'].value_counts().head(10)
plt.figure()
rating_count.plot(kind='pie', autopct='%1.1f%%')
plt.title('netflix rating distribution')
plt.ylabel('')
plt.savefig(PLOTS_DIR/ "Content_Distribution_by_Rating.png")
plt.show()


# trend of movies and tv shows added over the years
yearly_trend = df['year_added'].value_counts().sort_index()
plt.figure()
yearly_trend.plot(marker='o')
plt.title('Netflix content added by Years')
plt.xlabel('Year Added')
plt.ylabel('Number of Titles Added')
plt.savefig(PLOTS_DIR/ "Trend_of_Movies_and_TV_Shows_Added_Over_Years.png")
plt.show()

#which country has the most content

country_count = df['country'].str.split(',').explode().value_counts().head(10)
plt.figure()
country_count.plot(kind='bar', )
plt.title('Top 10 Countries with most netflix titles')
plt.xlabel('Country')
plt.ylabel('Number of Titles')
plt.xticks(rotation=25)
plt.savefig(PLOTS_DIR/ "Countries_with_Most_Content.png")
plt.show()


#top directors based on count of titles
director_count = df[df['director'] != "unknown"]['director'].value_counts().head(10)
plt.figure()
director_count.plot(kind='bar')
plt.title('Top 10 Directors featured on netflix')
plt.xlabel('Director')
plt.ylabel('Number of Titles')
plt.xticks(rotation=25)
plt.savefig(PLOTS_DIR/ "Top_Directors_on_Netflix.png")
plt.show()


print("all plots saved")
