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


def search(request):
    query = request.GET.get('q', '')
    selected_genres = request.GET.getlist('listed_in', [])
    year_filter = request.GET.get('year', '')
    country_filter = request.GET.get('country', '')
    sort_by = request.GET.get('sort', 'newest')

    results = NetflixTitle.objects.all()

    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(director__icontains=query) |
            Q(cast__icontains=query)
        )

    if selected_genres:
        genre_query = Q()
        for g in selected_genres:
            genre_query |= Q(listed_in__icontains=g)
        results = results.filter(genre_query)

    if year_filter:
        results = results.filter(release_year=year_filter)

    if country_filter:
        results = results.filter(country__icontains=country_filter)

    # Sorting options
    if sort_by == 'a-z':
        results = results.order_by('title')
    elif sort_by == 'z-a':
        results = results.order_by('-title')
    elif sort_by == 'oldest':
        results = results.order_by('release_year')
    else:  # newest
        results = results.order_by('-release_year')

    paginator = Paginator(results, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    genre_options = ["Action", "Adventure", "Anime", "Children", "Comedies",
                     "Documentaries", "Dramas", "Horror", "Independent",
                     "Music", "Romantic", "Sci-Fi", "Thrillers"]

    years = NetflixTitle.objects.values_list('release_year', flat=True).distinct().order_by('release_year')
    countries = NetflixTitle.objects.values_list('country', flat=True).distinct()

    return render(request, 'dashboard/search.html', {
        'page_obj': page_obj,
        'genre_options': genre_options,
        'years': years,
        'countries': countries,
        'query': query,
        'selected_genres': selected_genres,
        'year_filter': year_filter,
        'country_filter': country_filter,
        'sort_by': sort_by,
    })
