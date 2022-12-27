from django.db import models
from django.urls import reverse

# Create your models here.
class Book(models.Model):

    title = models.CharField(max_length=100, help_text='The title of the book')
    pub_date = models.DateField(help_text='The publication date')
    authors = models.ManyToManyField(Authors, through='full_name', help_text='The name(s) of the author(s)')
    summary = models.CharField(max_length=1000, help_text='A summary of the book\'s content')
    isbn = models.CharField(max_length=20, help_text='The ISBN number of the book', unique=True, primary_key=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.authors}"


class BookInstance(models.Model):
    """
    An instance of the book in the catalog. This refers to each individual book that can be lent out under each Book title.
    """
    uniqueId = models.CharField(max_length=20, help_text='The ID of the book in the catalog\'s stock', primary_key=True)
    due_back = models.DateTimeField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    imprint = models.CharField(max_length=30)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def status(self):
        if due_back:
            return 'Out on loan'
        else:
            return 'Available'

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

    name = models.CharField(max_length=30)

    def __str__(self):
        return name


class Language(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):
        return name
