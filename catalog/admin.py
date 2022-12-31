from django.contrib import admin

from .models import Book, BookInstance, Author, Genre, Language, User

# Register your models here.
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

class BookAdmin(admin.ModelAdmin):
    fields = [
        # 'title', 'authors', 'pub_date', 'isbn',
        # 'genre', 'language', 'summary'
    ]
    inlines = [BookInstanceInline]

admin.site.register(Book, BookAdmin)
# admin.site.register(BookInstance)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(User)