from django.db import models

# Create your models here.
class NetflixTitle(models.Model):

    show_id = models.CharField(max_length=255)
    type = models.CharField(max_length=50) 
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255, null=True, blank=True)
    cast = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateField(null=True, blank=True)
    release_year = models.IntegerField()
    rating = models.CharField(max_length=50, null=True, blank=True)
    duration = models.CharField(max_length=50)
    listed_in = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return F"{self.title} ,({self.release_year})"
    
