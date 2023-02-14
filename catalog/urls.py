from django.urls import path
from . import views


app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail-view'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail-view'),
    path('genres/', views.genres, name='genres'),
    path('languages/', views.languages, name='languages'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('booksloaned/', views.AllLoanedBooksLibrarianListView.as_view(), name='books-on-loan'),
    path('librarian/user/<int:pk>', views.manage_user, name='manage-user'),
]
