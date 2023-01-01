from django.contrib import admin

from .models import Book, BookInstance, Author, Genre, Language, User

# Register your models here.
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    fields = ('status', 'loaned_on', 'due_back')

class BookAdmin(admin.ModelAdmin):
    fields = [
        'title', 'authors', 'summary',
        ('isbn', 'genre', 'language')
    ]
    list_display = ('title', 'display_full_names', 'language')
    inlines = [BookInstanceInline]

class BookAuthorM2MInline(admin.TabularInline):
    model = Book.authors.through
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'death_date')
    fields = [
        'prefix', ('first_name', 'middle_names', 'last_name'),
        'suffix', ('birth_date', 'death_date')
    ]
    inlines = [BookAuthorM2MInline]


admin.site.register(Book, BookAdmin)
# admin.site.register(BookInstance)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(User)