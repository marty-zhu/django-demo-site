import re
import uuid

from datetime import date, timedelta
from django.utils import timezone

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    """
    Model representation of an author of a book.
    A book can have multiple authors and an author can have multiple books.
    """

    prefix = models.CharField(max_length=4, blank=True, null=True)
    first_name = models.CharField(max_length=20)
    middle_names = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    suffix = models.CharField(max_length=5, blank=True, null=True)

    name = models.CharField('search match string', max_length=69)

    birth_date = models.DateField('Born', blank=True, null=True)
    death_date = models.DateField('Died', blank=True, null=True)

    @property
    @admin.display(description='full name', ordering='last_name')
    def full_name(self):
        """
        Returns the full name representation of the author
        for terminal and admin console.
        """
        cn_pattern = re.compile(r'[\u4e00-\u9fff]+')
        if cn_pattern.search(self.last_name):
            return ' '.join([self.last_name, self.first_name])
        else:
            if self.middle_names:
                return ' '.join([self.first_name, self.middle_names, self.last_name])
            else:
                return ' '.join([self.first_name, self.last_name])

    class Meta:
        ordering = ['last_name', 'first_name', 'birth_date']

    def get_absolute_url(self):
        """Returns the URL to access a detailed record for this author."""
        return reverse("catalog:author-detail-view", kwargs={"pk": self.id})

    def __str__(self):
        """Human-readable string representation for validation."""
        return self.full_name

class Book(models.Model):
    """
    Model representation of a book with a unique ISBN,
    but not specific copies of it in stock.
    """

    title = models.CharField(max_length=200, help_text='The title of the book')
    pub_date = models.DateField(help_text='The publication date', blank=True, null=True)
    authors = models.ManyToManyField('Author', related_name='books', help_text='The name(s) of the author(s)')
    summary = models.CharField(max_length=2000, help_text='A summary of the book\'s content')
    isbn = models.IntegerField('ISBN', help_text='The ISBN number of the book', unique=True, primary_key=True, editable=False)
    genre = models.ManyToManyField('Genre', related_name='books', help_text='The genre(s) for this book')
    language = models.ForeignKey('Language', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        """Human-readable string representation for terminal validation."""
        names = [author.full_name for author in self.authors.all()]
        return f"{self.title} by {', '.join(names) if len(names) > 1 else names[0]}"

    @property
    @admin.display(description='author(s)')
    def display_full_names(self):
        """Show full names in the admin console list inline display."""
        names = [author.full_name for author in self.authors.all()]
        return ', '.join(names) if len(names) > 1 else names[0]

    @property
    def display_genres(self):
        """Show all genre categories the book covers."""
        genres = [genre.name for genre in self.genre.all()]
        return ', '.join(genres) if len(genres) > 1 else genres[0]

    def get_absolute_url(self):
        """Returns the URL to access a detailed record for this book."""
        return reverse('catalog:book-detail-view', kwargs={'pk': self.isbn})

    class Meta:
        ordering = ['title']


class BookInstance(models.Model):
    """
    An instance of the book in the catalog. In other words, a copy of the book in stock.
    This refers to each individual book that can be lent out under each Book title.
    """
    STATUS_MAINTENANCE = 'm'
    STATUS_LOANED = 'o'
    STATUS_AVAILABLE = 'a'
    STATUS_RESERVED = 'r'

    LOAN_STATUS = (
        (STATUS_MAINTENANCE, 'Maintenance'),
        (STATUS_LOANED, 'On Loan'),
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_RESERVED, 'Reserved'),
    )

    copy_id = models.UUIDField(default=uuid.uuid4, help_text='The ID of the book in the catalog\'s stock', primary_key=True, editable=False)
    loaned_on = models.DateTimeField(blank=True, null=True)
    due_back = models.DateTimeField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=200, blank=True)
    borrower = models.ForeignKey(User, blank=True, null=True, on_delete=models.RESTRICT)

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        default=STATUS_MAINTENANCE,
        help_text='Book availability status'
    )

    class Meta:

        ordering = ['status', 'loaned_on', 'due_back']
        permissions = (('can_mark_returned', 'Set book as returned'),)

    def __str__(self):
        """Human-readable string representation for validation."""
        copy_id = str(self.copy_id)
        return f"{self.book} with ID ending with ..{copy_id[-6:]}"

    def _update_status(self, status):
        """Helper method to update book status."""
        self.status=status

    def loan(self, period=None):
        """
        Automatically sets the loan out, due back, and status information
        when a book is being loaned out.

        Arguments:
            period [int]: the number of days to loan out.
        """
        if period is None:
            period = timedelta(days=14)
        else:
            period = timedelta(int(period))

        self.loaned_on = timezone.now()
        self.due_back = self.loaned_on + period
        self._update_status(self.STATUS_LOANED)
        return f"{self.book.title} {self.copy_id} loaned on {self.loaned_on}"

    @property
    def is_overdue(self):
        """Test if the book is overdue based on current date."""
        return bool(self.due_back.date() < date.today()) if self.due_back else False


class Genre(models.Model):
    """
    Model representation of the genres of the book.
    A book can cover multiple genres and a genre covers many books.
    """

    name = models.CharField(max_length=200, help_text='Enter a book genre')

    def __str__(self):
        """Human-readable string representation for validation."""
        return self.name


class Language(models.Model):
    """
    Model representation of the language the book is written in.
    """

    name = models.CharField(max_length=30)

    def __str__(self):
        """Human-readable string representation for validation."""
        return self.name


# class User(models.Model):
#     """
#     Model representation of a user who can borrow more than zero books.
#     """

#     prefix = models.CharField(max_length=4, blank=True, null=True)
#     first_name = models.CharField(max_length=20)
#     middle_initials = models.CharField(max_length=10, blank=True, null=True)
#     last_name = models.CharField(max_length=30)
#     suffix = models.CharField(max_length=5, blank=True, null=True)

#     @property
#     def full_name(self):
#         """Returns the full name representation of the user."""
#         if self.middle_initials:
#             return ' '.join([self.first_name, self.middle_initials, self.last_name])
#         else:
#             return ' '.join([self.first_name, self.last_name])

#     def __str__(self):
#         """Human-readable string representation for validation."""
#         return self.full_name
