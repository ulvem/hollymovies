"""hollymovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path


from viewer.views import (
    about_view, index,
    MoviesView, MovieCreateView, GenreCreateView, MovieUpdateView, MovieDeleteView,
    MovieDetailView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', about_view, name='about'),
    path("", index, name="index"),
    path("movies/", MoviesView.as_view(), name="movies"),
    path("add_genre/", GenreCreateView.as_view(), name="add_genre"),
    path("add_movie/", MovieCreateView.as_view(), name="add_movie"),
    path("update_movie/<pk>", MovieUpdateView.as_view(), name="update_movie"),
    path("delete_movie/<pk>", MovieDeleteView.as_view(), name="delete_movie"),
    path("movie_details/<pk>", MovieDetailView.as_view(), name="movie_details"),

    path('accounts/', include("accounts.urls", namespace="accounts")),
]




