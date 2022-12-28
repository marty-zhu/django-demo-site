import uuid

from django.db import models
from django.urls import reverse

# Create your models here.
class Author(models.Model):
    """
    Model representation of an author of a book.
    A book can have multiple authors and an author can have multiple books.
    """

    first_name = models.CharField(max_length=20)
    middle_initials = models.CharField(max_length=10, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField('Born', blank=True, null=True)
    death_date = models.DateField('Died', blank=True, null=True)

    @property
    def full_name(self):
        """Returns the full name representation of the author."""
        if self.middle_initials:
            return ' '.join([self.first_name, self.middle_initials, self.last_name])
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
    pub_date = models.DateField(help_text='The publication date')
    authors = models.ManyToManyField('Author', related_name='authors', help_text='The name(s) of the author(s)')
    summary = models.CharField(max_length=1000, help_text='A summary of the book\'s content')
    isbn = models.IntegerField('ISBN', help_text='The ISBN number of the book', unique=True, primary_key=True)
    genre = models.ManyToManyField('Genre', related_name='genres', help_text='The genre(s) for this book')
    language = models.ForeignKey('Language', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        """Human-readable string representation for validation."""
        return f"{self.title} by {self.authors[0].full_name}"

    def get_absolute_url(self):
        """Returns the URL to access a detailed record for this book."""
        return reverse('catalog:book-detail-view', kwargs={'pk': self.id})

    class Meta:
        ordering = ['isbn', 'title']


class BookInstance(models.Model):
    """
    An instance of the book in the catalog.
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

    copy_id = models.UUIDField(default=uuid.uuid4, help_text='The ID of the book in the catalog\'s stock', primary_key=True)
    loaned_on = models.DateTimeField(blank=True, null=True)
    due_back = models.DateTimeField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=200)
    borrower = models.ForeignKey('User', on_delete=models.RESTRICT)

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        default=STATUS_MAINTENANCE,
        help_text='Book availability status'
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """Human-readable string representation for validation."""
        return f"{self.book} with ID {self.copy_id}"


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


class User(models.Model):
    """
    Model representation of a user who can borrow more than zero books.
    """

    first_name = models.CharField(max_length=20)
    middle_initials = models.CharField(max_length=10, blank=True, null=True)
    last_name = models.CharField(max_length=30)

    @property
    def full_name(self):
        """Returns the full name representation of the user."""
        if self.middle_initials:
            return ' '.join([self.first_name, self.middle_initials, self.last_name])
        else:
            return ' '.join([self.first_name, self.last_name])

    def __str__(self):
        """Human-readable string representation for validation."""
        return self.full_name
