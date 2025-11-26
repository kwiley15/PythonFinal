
# # Create your views here.
# from django.shortcuts import render
# from .models import NetflixTitle
# from django.db.models import Count
# from django.core.paginator import Paginator
# import matplotlib.pyplot as plt
# import io
# import urllib, base64

# # Homepage
# def index(request):
#     return render(request, 'dashboard/index.html')


# # Genre distribution plot
# def genre_plot(request):
#     listed_in = NetflixTitle.objects.values('listed_in').annotate(count=Count('listed_in')).order_by('-count')
#     labels = [g['listed_in'] for g in listed_in]
#     counts = [g['count'] for g in listed_in]

#     plt.figure(figsize=(10,6))
#     plt.bar(labels, counts, color='skyblue')
#     plt.xticks(rotation=90)
    

#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)
#     string = base64.b64encode(buf.read())
#     uri = urllib.parse.quote(string)
#     return render(request, 'dashboard/genre_plot.html', {'data': uri})

# # Search page with pagination

# def search(request):
#     query = request.GET.get('q', '')
#     genre_filter = request.GET.get('listed_in', '')
#     year_filter = request.GET.get('year', '')
#     country_filter = request.GET.get('country', '')

#     results = NetflixTitle.objects.all()

#     if query:
#         results = results.filter(title__icontains=query)
#     if genre_filter:
#         results = results.filter(listed_in=genre_filter)
#     if year_filter:
#         results = results.filter(release_year=year_filter)
#     if country_filter:
#         results = results.filter(country=country_filter)

#     # Pagination
#     paginator = Paginator(results, 20)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Dropdown data
#     Listed_in = NetflixTitle.objects.values_list('listed_in', flat=True).distinct()
#     years = NetflixTitle.objects.values_list('release_year', flat=True).distinct().order_by('release_year')
#     countries = NetflixTitle.objects.values_list('country', flat=True).distinct()

#     return render(request, 'dashboard/search.html', {
#         'page_obj': page_obj,
#         'listed_in': Listed_in,
#         'years': years,
#         'countries': countries,
#         'query': query,
#         'genre_filter': genre_filter,
#         'year_filter': year_filter,
#         'country_filter': country_filter
#     })


# from django.shortcuts import render
# from .models import NetflixTitle
# from django.db.models import Count, Q
# from django.core.paginator import Paginator
# import matplotlib
# matplotlib.use('Agg')  # safe backend
# import matplotlib.pyplot as plt
# import io, urllib, base64
# import pandas as pd

# # Homepage
# def index(request):
#     return render(request, 'dashboard/index.html')


# # Genre plot (split multiple genres)
# def genre_plot(request):
#     # Split genres and count
#     all_genres = NetflixTitle.objects.values_list('listed_in', flat=True)
#     genre_list = []
#     for g in all_genres:
#         genre_list.extend([x.strip() for x in g.split(',')])
    
#     genre_counts = pd.Series(genre_list).value_counts().head(10)

#     plt.figure(figsize=(10,6))
#     genre_counts.plot(kind='bar', color='skyblue')
#     plt.xticks(rotation=45)
#     plt.tight_layout()

#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)
#     string = base64.b64encode(buf.read())
#     uri = urllib.parse.quote(string)
#     return render(request, 'dashboard/genre_plot.html', {'data': uri})


# # Search page with multi-field search, filters, pagination
# def search(request):
#     query = request.GET.get('q', '')
#     genre_filter = request.GET.get('listed_in', '')
#     year_filter = request.GET.get('year', '')
#     country_filter = request.GET.get('country', '')

#     results = NetflixTitle.objects.all()

#     # Multi-field search
#     if query:
#         results = results.filter(
#             Q(title__icontains=query) |
#             Q(director__icontains=query) |
#             Q(cast__icontains=query)
#         )

#     # Filters
#     if genre_filter:
#         results = results.filter(listed_in__icontains=genre_filter)
#     if year_filter:
#         results = results.filter(release_year=year_filter)
#     if country_filter:
#         results = results.filter(country__icontains=country_filter)

#     results = results.order_by('-release_year', 'title')

#     # Pagination
#     paginator = Paginator(results, 20)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Dropdown data
#     listed_in_choices = NetflixTitle.objects.values_list('listed_in', flat=True).distinct()
#     years = NetflixTitle.objects.values_list('release_year', flat=True).distinct().order_by('release_year')
#     countries = NetflixTitle.objects.values_list('country', flat=True).distinct()

#     return render(request, 'dashboard/search.html', {
#         'page_obj': page_obj,
#         'listed_in': listed_in_choices,
#         'years': years,
#         'countries': countries,
#         'query': query,
#         'genre_filter': genre_filter,
#         'year_filter': year_filter,
#         'country_filter': country_filter
#     })
from django.shortcuts import render
from .models import NetflixTitle
from django.db.models import Q
from django.core.paginator import Paginator

# Homepage
def index(request):
    return render(request, 'dashboard/index.html')


# Plots page using static images
def genre_plot(request):
    """
    Display all 5 Netflix analysis plots from static images.
    """
    return render(request, 'dashboard/genre_plot.html')


# Search page with multi-field search, filters, pagination
def search(request):
    query = request.GET.get('q', '')
    genre_filter = request.GET.get('listed_in', '')
    year_filter = request.GET.get('year', '')
    country_filter = request.GET.get('country', '')

    results = NetflixTitle.objects.all()

    # Multi-field search (title, director, cast)
    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(director__icontains=query) |
            Q(cast__icontains=query)
        )

    # Filters
    if genre_filter:
        results = results.filter(listed_in__icontains=genre_filter)
    if year_filter:
        results = results.filter(release_year=year_filter)
    if country_filter:
        results = results.filter(country__icontains=country_filter)

    results = results.order_by('-release_year', 'title')

    # Pagination
    paginator = Paginator(results, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Dropdown/filter data
    listed_in_choices = NetflixTitle.objects.values_list('listed_in', flat=True).distinct()
    years = NetflixTitle.objects.values_list('release_year', flat=True).distinct().order_by('release_year')
    countries = NetflixTitle.objects.values_list('country', flat=True).distinct()

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

