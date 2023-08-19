from django.test import TestCase
from django.urls import reverse

from catalog.models import *


class TestAuthorListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        num_authors = 13
        
        for author_id in range(num_authors):
            Author.objects.create(
                first_name = 'Test',
                last_name = f"Author{author_id}"
            )

        test_user = User.objects.create_user(
            username = 'test_user',
            password = 'fortesting'
        )
        test_user.save()

    def setUp(self):
        self.client.login(
            username = 'test_user',
            password = 'fortesting',
        )
        
    def test_url_accessible_by_locator(self):
        resp = self.client.get('/catalog/authors/')
        self.assertEqual(resp.status_code, 200)

    def test_url_accessible_by_name(self):
        resp = self.client.get(reverse('catalog:authors'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template_is_correct(self):
        pass

    def test_pagination_is_ten(self):
        pass

    def test_view_list_all_authors(self):
        pass