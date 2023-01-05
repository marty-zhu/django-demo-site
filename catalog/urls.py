from django.urls import path
from . import views


app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.authors, name='authors'),
    path('genres/', views.genres, name='genres'),
    path('languages/', views.languages, name='languages'),
]
