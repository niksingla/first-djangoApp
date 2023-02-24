from django.urls import path
from . import open_feature as ft_views
from .apis.movies import getmovie
from . import top_imdb 

urlpatterns = [
    path('features/<str:features>/', ft_views.open_feature),
    path('apis/entertainment/', getmovie.get_json_data),
    path('features/entertainment/top-imdb', top_imdb.topImdb),
]

