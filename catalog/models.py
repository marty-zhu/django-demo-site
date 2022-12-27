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
