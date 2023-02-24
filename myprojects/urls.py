from django.urls import path
from . import views, browse
from cool_fts.apis.movies import imdbtrailer

urlpatterns = [
    path('projects/', views.projects),
    path('projects/screen', views.screen),
    path('features/entertainment/browse', browse.browse),
    path('apis/imdb-trailer/',imdbtrailer.trailerAPI)
]