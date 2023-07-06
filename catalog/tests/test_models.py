from django.test import TestCase
from catalog.models import *

from freezegun import freeze_time
from datetime import date, timedelta
from django.utils import timezone

class TestAuthorModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(
            prefix = 'Sir',
            first_name = 'Test',
            last_name = 'Case',
            suffix = 'Sr'
        )

    def test_prefix_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('prefix').verbose_name
        self.assertEqual(field_label, 'prefix')

    def test_prefix_max_length(self):
        author = Author.objects.get(id=1)
        max_len = author._meta.get_field('prefix').max_length
        self.assertEqual(max_len, 4)

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_len = author._meta.get_field('first_name').max_length
        self.assertEqual(max_len, 20)

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_len = author._meta.get_field('last_name').max_length
        self.assertEqual(max_len, 30)

    def test_suffix_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('suffix').verbose_name
        self.assertEqual(field_label, 'suffix')

    def test_suffix_max_length(self):
        author = Author.objects.get(id=1)
        max_len = author._meta.get_field('suffix').max_length
        self.assertEqual(max_len, 5)

    def test_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'search match string')

    def test_name_max_length(self):
        author = Author.objects.get(id=1)
        max_len = author._meta.get_field('name').max_length
        self.assertEqual(max_len, 69)

    def test_birth_date_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('birth_date').verbose_name
        self.assertEqual(field_label, 'Born')

    def test_death_date_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('death_date').verbose_name
        self.assertEqual(field_label, 'Died')

    def test_object_name_is_first_name_last_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.first_name} {author.last_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/catalog/authors/1')


class TestBookModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(
            first_name = "Test",
            last_name = "Author",
        )
        Genre.objects.create(
            name = "Test",
        )
        Language.objects.create(
            name = "Test",
        )
        Book.objects.create(
            title = "Test Book",
            pub_date = date(year=1900, month=1, day=1),
            summary = "Test case for Book object",
            isbn = 123456789,
        )
        book = Book.objects.get(isbn=123456789)
        author = Author.objects.get(id=1)
        genre = Genre.objects.get(id=1)
        lang = Language.objects.get(id=1)
        book.authors.add(author)
        book.genre.add(genre)
        book.language = lang
        book.save()

    def test_title_label(self):
        book = Book.objects.get(isbn=123456789)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        book = Book.objects.get(isbn=123456789)
        max_len = book._meta.get_field('title').max_length
        self.assertEqual(max_len, 200)

    def test_title_help_text(self):
        book = Book.objects.get(isbn=123456789)
        help_text = book._meta.get_field('title').help_text
        self.assertEqual(help_text, 'The title of the book')

    def test_pub_date_label(self):
        book = Book.objects.get(isbn=123456789)
        field_label = book._meta.get_field('pub_date').verbose_name
        self.assertEqual(field_label, 'pub date')

    def test_pub_date_help_text(self):
        book = Book.objects.get(isbn=123456789)
        help_text = book._meta.get_field('pub_date').help_text
        self.assertEqual(help_text, 'The publication date')

    def test_author_label(self):
        book = Book.objects.get(isbn=123456789)
        field_label = book._meta.get_field('authors').verbose_name
        self.assertEqual(field_label, 'authors')

    def test_author_help_text(self):
        book = Book.objects.get(isbn=123456789)
        help_text = book._meta.get_field('authors').help_text
        self.assertEqual(help_text, 'The name(s) of the author(s)')

    def test_author_related_name(self):
        book = Book.objects.get(isbn=123456789)
        related_name = book._meta.get_field('authors')._related_name
        self.assertEqual(related_name, 'books')

    def test_summary_label(self):
        book = Book.objects.get(isbn=123456789)
        field_label = book._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'summary')

    def test_summary_max_length(self):
        book = Book.objects.get(isbn=123456789)
        max_len = book._meta.get_field('summary').max_length
        self.assertEqual(max_len, 2000)

    def test_summary_help_text(self):
        book = Book.objects.get(isbn=123456789)
        help_text = book._meta.get_field('summary').help_text
        self.assertEqual(help_text, 'A summary of the book\'s content')

    def test_isbn_label(self):
        book = Book.objects.get(isbn=123456789)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'ISBN')

    def test_isbn_help_text(self):
        book = Book.objects.get(isbn=123456789)
        help_text = book._meta.get_field('isbn').help_text
        self.assertEqual(help_text, 'The ISBN number of the book')

    def test_genre_label(self):
        book = Book.objects.get(isbn=123456789)
        field_label = book._meta.get_field('genre').verbose_name
        self.assertEqual(field_label, 'genre')

    def test_genre_related_name(self):
        book = Book.objects.get(isbn=123456789)
        related_name = book._meta.get_field('genre')._related_name
        self.assertEqual(related_name, 'books')

    def test_genre_help_text(self):
        book = Book.objects.get(isbn=123456789)
        help_text = book._meta.get_field('genre').help_text
        self.assertEqual(help_text, 'The genre(s) for this book')

    def test_language_label(self):
        book = Book.objects.get(isbn=123456789)
        field_label = book._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_book_has_author(self):
        book = Book.objects.get(isbn=123456789)
        self.assertEqual(book.authors.count(), 1)

    def test_book_has_genre(self):
        book = Book.objects.get(isbn=123456789)
        self.assertEqual(book.genre.count(), 1)

    def test_book_has_language(self):
        book = Book.objects.get(isbn=123456789)
        lang = Language.objects.get(id=1)
        self.assertEqual(book.language, lang)


class TestBookInstanceModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(
            first_name = 'Test',
            last_name = 'Author',
        )
        cls.book = Book.objects.create(
            title = 'Test Book',
            pub_date = date(year=1900, month=1, day=1),
            summary = "Test case for Book object",
            isbn = 123456789,
        )
        cls.book.authors.add(cls.author)
        cls.book.save()
        cls.borrower = User.objects.create(
            username = 'testuser',
        )
        cls.book_instance = BookInstance.objects.create(
            book = cls.book,
            borrower = cls.borrower,
        )
        cls.book_instance.save()

    def test_book_instance_labels(self):
        self.assertEqual(
            self.book_instance._meta.get_field('copy_id').name,
            'copy_id'
        )
        self.assertEqual(
            self.book_instance._meta.get_field('loaned_on').name,
            'loaned_on'
        )
        self.assertEqual(
            self.book_instance._meta.get_field('due_back').name,
            'due_back'
        )
        self.assertEqual(
            self.book_instance._meta.get_field('book').name,
            'book'
        )
        self.assertEqual(
            self.book_instance._meta.get_field('imprint').name,
            'imprint'
        )
        self.assertEqual(
            self.book_instance._meta.get_field('borrower').name,
            'borrower'
        )
        self.assertEqual(
            self.book_instance._meta.get_field('status').name,
            'status'
        )

    def test_book_instance_string(self):
        expected_string = \
            f"{self.book_instance.book} with ID ending with ..{str(self.book_instance.copy_id)[-6:]}"
        self.assertEqual(str(self.book_instance), expected_string)

    def test_book_instance_update_status(self):
        self.book_instance._update_status(
            self.book_instance.STATUS_AVAILABLE)
        self.assertEqual(
            self.book_instance.status, self.book_instance.STATUS_AVAILABLE)

    @freeze_time("2023-01-01")
    def test_book_instance_default_loan_method(self):
        self.book_instance.loan()
        self.assertEqual(
            self.book_instance.loaned_on, timezone.now()
        )
        self.assertEqual(
            self.book_instance.due_back, timezone.now() + \
                timedelta(days=14)
        )
        self.assertEqual(
            self.book_instance.status, self.book_instance.STATUS_LOANED
        )

    @freeze_time("2023-01-01")
    def test_book_instance_custom_loan_time(self):
        self.book_instance.loan(period=7)
        self.assertEqual(
            self.book_instance.loaned_on, timezone.now()
        )
        self.assertEqual(
            self.book_instance.due_back, timezone.now() + \
                timedelta(days=7)
        )
        self.assertEqual(
            self.book_instance.status, self.book_instance.STATUS_LOANED
        )

    def test_book_instance_is_overdue_true(self):
        with freeze_time("2023-01-01"):
            self.book_instance.loan()
        self.assertTrue(self.book_instance.is_overdue)
    
    def test_book_instance_is_overdue_false(self):
        self.book_instance.loan()
        self.assertFalse(self.book_instance.is_overdue)
    

class TestGenreModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(
            name = 'Test Genre'
        )

    def test_model_labels(self):
        genre = Genre.objects.get(id=1)
        field_name = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_name, 'name')

    def test_model_name_max_length(self):
        genre = Genre.objects.get(id=1)
        length = genre._meta.get_field('name').max_length
        self.assertEqual(length, 200)

    def test_name_field_help_text(self):
        genre = Genre.objects.get(id=1)
        help_text = genre._meta.get_field('name').help_text
        self.assertEqual(help_text, 'Enter a book genre')

    def test_model_string(self):
        genre = Genre.objects.get(id=1)
        string = str(genre)
        self.assertEqual(string, 'Test Genre')