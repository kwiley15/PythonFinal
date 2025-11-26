
# Create your views here.
from django.shortcuts import render
from .models import NetflixTitle
from django.db.models import Count
from django.core.paginator import Paginator
import matplotlib.pyplot as plt
import io
import urllib, base64

# Homepage
def index(request):
    return render(request, 'dashboard/index.html')


# Genre distribution plot
def genre_plot(request):
    genres = NetflixTitle.objects.values('genre').annotate(count=Count('genre')).order_by('-count')
    labels = [g['genre'] for g in genres]
    counts = [g['count'] for g in genres]

    plt.figure(figsize=(10,6))
    plt.bar(labels, counts, color='skyblue')
    plt.xticks(rotation=90)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request, 'dashboard/genre_plot.html', {'data': uri})

# Search page with pagination

def search(request):
    query = request.GET.get('q', '')
    genre_filter = request.GET.get('genre', '')
    year_filter = request.GET.get('year', '')
    country_filter = request.GET.get('country', '')

    results = NetflixTitle.objects.all()

    if query:
        results = results.filter(title__icontains=query)
    if genre_filter:
        results = results.filter(genre=genre_filter)
    if year_filter:
        results = results.filter(release_year=year_filter)
    if country_filter:
        results = results.filter(country=country_filter)

    # Pagination
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Dropdown data
    genres = NetflixTitle.objects.values_list('genre', flat=True).distinct()
    years = NetflixTitle.objects.values_list('release_year', flat=True).distinct().order_by('release_year')
    countries = NetflixTitle.objects.values_list('country', flat=True).distinct()

    return render(request, 'dashboard/search.html', {
        'page_obj': page_obj,
        'genres': genres,
        'years': years,
        'countries': countries,
        'query': query,
        'genre_filter': genre_filter,
        'year_filter': year_filter,
        'country_filter': country_filter
    })