from django.test import TestCase
from catalog.models import *


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
        Book.objects.create(
            title = "Test Book",
            pub_date = date(year=1900, month=1, day=1),
            authors = Author.objects.create(
                first_name="Test", last_name="Case",
            ),
            summary = "Test case for Book object",
            isbn = 123456789,
            genre = Genre(name='Testing'),
            language = Language(name='Python'),
        )

    def test_title_label(self):
        pass

    def test_title_max_length(self):
        pass

    def test_title_help_text(self):
        pass

    def test_pub_date_label(self):
        pass

    def test_pub_date_help_text(self):
        pass

    def test_author_label(self):
        pass

    def test_author_help_text(self):
        pass

    def test_summary_label(self):
        pass

    def test_summary_max_length(self):
        pass

    def test_summary_help_text(self):
        pass

    def test_isbn_label(self):
        pass

    def test_isbn_help_text(self):
        pass

    def test_genre_label(self):
        pass

    def test_genre_help_text(self):
        pass

    def test_genre_related_name(self):
        pass

    def test_language_label(self):
        pass
