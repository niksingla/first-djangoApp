from django.db import models

# Create your models here.
class searchData(models.Model):
    query = models.CharField(max_length=100)
    updatedOn = models.DateTimeField()
    added = models.DateTimeField()
    results = models.TextField()

    def __str__(self):
        return self.query

class trailerDB(models.Model):
    title = models.CharField(max_length=100)
    updatedOn = models.DateTimeField()
    trailer = models.CharField(max_length=2000)
    imdbID = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.title