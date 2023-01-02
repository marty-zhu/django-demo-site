from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import *

# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_language = Language.objects.all().count()
    template = loader.get_template('catalog/index.html')
    context = {
        'num_books': num_books,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_language': num_language,
    }
    return HttpResponse(template.render(context, request))