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
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),  # TODO: change to `member/mybooks`.
    path('librarian/booksloaned/', views.AllLoanedBooksLibrarianListView.as_view(), name='books-on-loan'),
    path('librarian/user/<str:username>', views.manage_member, name='librarian-manage-member'),
    path('librarian/book/<uuid:copy_id>/renew/', views.renew_book_librarian, name='librarian-renew-book'),
    path('librarian/add/user', views.librarian_add_user, name='librarian-add-user'),
    # path('librarian/books/add', ) # TODO: add librarian add book
]
