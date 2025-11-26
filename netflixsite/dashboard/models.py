from django.db import models

# Create your models here. this represents the structure of the netflix titles data in the database
class NetflixTitle(models.Model):

    show_id = models.CharField(max_length=255) # unique identifier for each show
    type = models.CharField(max_length=50) # type of show (movie or tv show)
    title = models.CharField(max_length=255)# title of the show or movie 
    director = models.CharField(max_length=255) # director of the show or movie
    cast = models.TextField(null=True, blank=True) # cast members, can be null or blank
    country = models.CharField(max_length=255) # country of origin
    date_added = models.DateField(null=True, blank=True) # date when added to netflix, can be null or blank
    release_year = models.IntegerField() # year of release
    rating = models.CharField(max_length=50) # content rating
    duration = models.CharField(max_length=50) # duration of the show or movie
    listed_in = models.CharField(max_length=255) # genres or categories its listed in 
    description = models.TextField() # description of the show or movie

    def __str__(self): # string representation of the model
        return F"{self.title} ,({self.release_year})"
        # returns title and release year when the object is printed
    
