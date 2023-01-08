from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views import generic

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

class BookListView(generic.ListView):
    model = Book
    template_name = 'catalog/books.html'
    context_object_name = 'list_of_all_books'
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_details.html'
    context_object_name = 'book_detail_info'

class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/authors.html'
    context_object_name = 'list_of_all_authors'
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_details.html'
    context_object_name = 'author'

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