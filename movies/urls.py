from django.urls import path, include
from movies.views import MoviesView, MoviesByIdView, MoviesOrdersView

urlpatterns = [
    path('movies/', MoviesView.as_view()),
    path('movies/<int:movie_id>/', MoviesByIdView.as_view()),
    path('movies/<int:movie_id>/orders/', MoviesOrdersView.as_view()),
]
