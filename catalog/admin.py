import logging

from django import forms
from django.contrib import admin
from django.utils.encoding import force_str

from .models import Book, BookInstance, Author, Genre, Language #, User

logging.basicConfig(filename='admin_debug.log', filemode='w', level=logging.DEBUG)

# Register your models here.
class DebugAdminForm(forms.ModelForm):

    def is_valid(self):
        logging.debug(force_str(self.errors))
        return super(DebugAdminForm, self).is_valid()

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    fields = ('status', 'loaned_on', 'due_back', 'borrower')
    form = DebugAdminForm

class BookAdmin(admin.ModelAdmin):
    form = DebugAdminForm
    readonly_fields = ('isbn',)
    fields = [
        'title', 'authors', 'summary', 'isbn',
        ('genre', 'language')
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
admin.site.register(BookInstance)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)