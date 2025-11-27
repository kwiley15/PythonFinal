from django.shortcuts import render # Import render 
from .models import NetflixTitle # import netflixsite model for database queries 
from django.db.models import Q # Import Q for complex queries 
from django.core.paginator import Paginator # import this for large dataset control
import pandas as pd # import pandas to work with csv 
from pathlib import Path # path to handle files 

# Load cleaned data for homepage display
# this data is only used for the home page to make it look not so blank,
# (not database querying which is done in search view)
CLEANED_CSV_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "cleaned_netflix_titles.csv"
df = pd.read_csv(CLEANED_CSV_PATH)



# Homepage
def index(request):
    #convert dataframe to list of lists for easier rendering in template
    data = df.values.tolist()  # just the row values
    columns = df.columns.tolist()  # column headers

    paginator = Paginator(data, 10)  # 10 rows per page
    page_number = request.GET.get('page') # get current page from URL query parameters
    page_obj = paginator.get_page(page_number) # get the page object

    #send table data to template
    context = {
        "columns": columns,
        "page_obj": page_obj,
    }
    return render(request, 'dashboard/index.html', context)


# Plots page using static images
def genre_plot(request): 
   # Display all 5 Netflix analysis plots from static images.
    #this simply renders the template with the patplotlib generated images
    return render(request, 'dashboard/genre_plot.html')


def search(request):
    query = request.GET.get('q', '') # user search input for title , director , cast default is nothing 
    selected_genres = request.GET.getlist('listed_in', []) # list of genres selected by the user emtpy by deafult 
    year_filter = request.GET.get('year', '') # filter for release year 
    country_filter = request.GET.get('country', '') # filter for country 
    sort_by = request.GET.get('sort', 'newest') # sorting option default is newest 

    results = NetflixTitle.objects.all() # queryset containing all netflix title records 

    if query:
        # filter titles where title , director or cast contains the search string 
        results = results.filter(
            Q(title__icontains=query) |
            Q(director__icontains=query) |
            Q(cast__icontains=query)
        )

    if selected_genres: 
        genre_query = Q() # start an empty Q object for OR conditions 
        for g in selected_genres: # and an or condition for each selected genre 
            genre_query |= Q(listed_in__icontains=g)
        results = results.filter(genre_query) # filter the results by the combined genre or conditions 

    if year_filter: # filter by release year if provided 
        results = results.filter(release_year=year_filter)

    if country_filter: # filter by country if provdied 
        results = results.filter(country__icontains=country_filter)

    # Sorting options
    if sort_by == 'a-z':
        results = results.order_by('title') # A-Z
    elif sort_by == 'z-a':
        results = results.order_by('-title') # Z-A
    elif sort_by == 'oldest':
        results = results.order_by('release_year') # oldest first 
    else:  # newest
        results = results.order_by('-release_year') # newest first 

    paginator = Paginator(results, 20) # 20 rows per page 
    page_number = request.GET.get('page') # get current page number from URL query string 
    page_obj = paginator.get_page(page_number) # returns page object for templates rendering 

    genre_options = ["Action", "Adventure", "Anime", "Children", "Comedies", # options for checkboxes 
                     "Documentaries", "Dramas", "Horror", "Independent",
                     "Music", "Romantic", "Sci-Fi", "Thrillers"]

    years = NetflixTitle.objects.values_list('release_year', flat=True).distinct().order_by('release_year') # get all unique years in the database for filter dropdown 
    countries = NetflixTitle.objects.values_list('country', flat=True).distinct() # get all the countrys in the database for the filter dropdown 
 
    return render(request, 'dashboard/search.html', {
        'page_obj': page_obj, #paginated results for current page
        'genre_options': genre_options, # available genre filters
        'years': years, # available year filtes
        'countries': countries, #available country filters
        'query': query, # current search query (inputs keep values through pages) 
        'selected_genres': selected_genres, # currently selected genres
        'year_filter': year_filter, # currently selected year filter
        'country_filter': country_filter, # currently selected country filter 
        'sort_by': sort_by, # current sort option 
    })
