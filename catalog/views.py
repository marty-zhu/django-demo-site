from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import *

# Create your views here.
def index(request):
    list_of_all_books = Book.objects.all()
    template = loader.get_template('catalog/index.html')
    context = {
        'list_of_all_books': list_of_all_books,
    }
    return HttpResponse(template.render(context, request))