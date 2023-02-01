from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import *

# Create your views here.
# TODO: refactor to generic views to reduce redundancy
def index(request):
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_language = Language.objects.all().count()
    template = loader.get_template('catalog/index.html')
    
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_language': num_language,
        'num_visits': num_visits,
    }
    return HttpResponse(template.render(context, request))

# Switched to Class-based views
#
# def books(request):
#     list_of_all_books = Book.objects.all()
#     template = loader.get_template('catalog/books.html')
#     context = {
#         'list_of_all_books': list_of_all_books,
#     }
#     return HttpResponse(template.render(context, request))

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = 'catalog/books.html'
    context_object_name = 'list_of_all_books'
    paginate_by = 10

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'catalog/book_details.html'
    context_object_name = 'book_detail_info'

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    template_name = 'catalog/authors.html'
    context_object_name = 'list_of_all_authors'
    paginate_by = 10

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = 'catalog/author_details.html'
    context_object_name = 'author'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
                borrower=self.request.user
            ).filter(
                status__exact='o'
            ).order_by('due_back')

class AllLoanedBooksLibrarianListView(PermissionRequiredMixin, generic.ListView):
    permission_required = ('catalog.can_mark_returned',)

    model = BookInstance
    template_name = 'catalog/bookinstance_on_loan_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            status__exact='o'
        ).order_by('due_back')
    

def genres(request):
    list_of_all_genres = Genre.objects.all()
    template = loader.get_template('catalog/genres.html')
    context = {
        'list_of_all_genres': list_of_all_genres,
    }
    return HttpResponse(template.render(context, request))

def languages(request):
    list_of_all_languages = Language.objects.all()
    template = loader.get_template('catalog/languages.html')
    context = {
        'list_of_all_languages': list_of_all_languages,
    }
    return HttpResponse(template.render(context, request))