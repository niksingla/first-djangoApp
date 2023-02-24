from django.urls import path
from . import views
from .apis import views as api_views
from cool_fts import open_feature as ft_views


urlpatterns = [
    path('',views.home),
    path('login/', views.message),
    path('register/', views.register),
    path('signout', views.signout),
    path('signin', views.signin),
    path('contact', views.contact),
    path('features/', views.features),
    path('signup', views.signup),
    path('profile', views.profile),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    
    path('apis/home-content', api_views.home_content_api)
]

