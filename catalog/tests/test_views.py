from django.test import TestCase

from catalog.models import *


class TestAuthorListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        num_authors = 13
        
        for author_id in range(num_authors):
            Author.create(
                first_name = 'Test',
                last_name = f"Author{author_id}"
            )
    
    def test_url_accessible_by_locator(self):
        pass

    def test_url_accessible_by_name(self):
        pass

    def test_view_template_is_correct(self):
        pass

    def test_pagination_is_ten(self):
        pass

    def test_view_list_all_authors(self):
        pass