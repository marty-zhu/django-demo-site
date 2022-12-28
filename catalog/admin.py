from django.contrib import admin

from .models import Book, BookInstance, Authors, Genre, Language, User

# Register your models here.
admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Authors)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(User)