from django.shortcuts import render
from .models import NetflixTitle
from django.db.models import Q
from django.core.paginator import Paginator
import pandas as pd
from pathlib import Path

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
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #send table data to template
    context = {
        "columns": columns,
        "page_obj": page_obj,
    }
    return render(request, 'dashboard/index.html', context)


# Plots page using static images
def genre_plot(request):
    """
    Display all 5 Netflix analysis plots from static images.
    """
    #this simply renders the template with the patplotlib generated images
    return render(request, 'dashboard/genre_plot.html')


# Search page with multi-field search, filters, pagination
def search(request):
    # capture search query and filters from GET parameters
    query = request.GET.get('q', '')
    genre_filter = request.GET.get('listed_in', '')
    year_filter = request.GET.get('year', '')
    country_filter = request.GET.get('country', '')

    #start with all the database entries
    results = NetflixTitle.objects.all()

    # Multi-field search (title, director, cast)
    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(director__icontains=query) |
            Q(cast__icontains=query)
        )

    # apply filter if user selected any 
    if genre_filter:
        results = results.filter(listed_in__icontains=genre_filter)
    if year_filter:
        results = results.filter(release_year=year_filter)
    if country_filter:
        results = results.filter(country__icontains=country_filter)

    # Order results by release year (newest first) then title
    results = results.order_by('-release_year', 'title')

    # Pagination 
    paginator = Paginator(results, 20) # 20 results per page
    page_number = request.GET.get('page') # get current page number from request
    page_obj = paginator.get_page(page_number) # get the page object for the current page

    # Dropdown/filter data (distinct values from database)
    listed_in_choices = NetflixTitle.objects.values_list('listed_in', flat=True).distinct()
    years = NetflixTitle.objects.values_list('release_year', flat=True).distinct().order_by('release_year')
    countries = NetflixTitle.objects.values_list('country', flat=True).distinct()
    
    #send results and filter values back to the search template
    return render(request, 'dashboard/search.html', {
        'page_obj': page_obj,
        'listed_in': listed_in_choices,
        'years': years,
        'countries': countries,
        'query': query,
        'genre_filter': genre_filter,
        'year_filter': year_filter,
        'country_filter': country_filter
    })

