import uuid

from django.db import models
from django.urls import reverse

# Create your models here.
class Book(models.Model):

    title = models.CharField(max_length=200, help_text='The title of the book')
    pub_date = models.DateField(help_text='The publication date')
    authors = models.ManyToManyField('Authors', through='full_name', help_text='The name(s) of the author(s)', null=True)
    summary = models.CharField(max_length=1000, help_text='A summary of the book\'s content')
    isbn = models.CharField('ISBN', max_length=13, help_text='The ISBN number of the book', unique=True, primary_key=True)
    genre = models.ManyToManyField('Genre', help_text='The genre(s) for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title} by {self.authors}"

    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.isbn)])

    class Meta:
        ordering = ['isbn', 'title']


class BookInstance(models.Model):
    """
    An instance of the book in the catalog. This refers to each individual book that can be lent out under each Book title.
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

    id = models.UUIDField(default=uuid.uuid4, help_text='The ID of the book in the catalog\'s stock', primary_key=True)
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
        return f"{self.book} with ID {self.uniqueId}"


class Authors(models.Model):

    first_name = models.CharField(max_length=20)
    middle_initials = models.CharField(max_length=10)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    death_date = models.DateField()

    @property
    def full_name(self):
        if middle_initials:
            return ' '.join([self.first_name, self.middle_initials, self.last_name])
        else:
            return ' '.join([self.first_name, self.last_name])

    def __str__(self):
        return self.full_name


class Genre(models.Model):

    name = models.CharField(max_length=200, help_text='Enter a book genre')

    def __str__(self):
        return self.name


class Language(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class User(models.Model):

    first_name = models.CharField(max_length=20)
    middle_initials = models.CharField(max_length=10)
    last_name = models.CharField(max_length=30)

    @property
    def full_name(self):
        if middle_initials:
            return ' '.join([self.first_name, self.middle_initials, self.last_name])
        else:
            return ' '.join([self.first_name, self.last_name])

    def __str__(self):
        return self.full_name
