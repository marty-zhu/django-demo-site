from django.test import TestCase
from django.urls import reverse

from catalog.models import *


class TestLoginRedirect(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        num_authors = 3
        for author_id in range(num_authors):
            Author.objects.create(
                first_name = 'Test',
                last_name = f'Author{author_id}'
            )
        
        test_user = User.objects.create_user(
            username = 'test_user',
            password = 'fortesting',
        )
        test_user.save()

    def test_correct_not_logged_in_redirect(self):
        resp = self.client.get(reverse('catalog:authors'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(
            resp, '/accounts/login/?next=/catalog/authors/'
            )

    def test_login(self):
        self.client.login(
            username = 'test_user',
            password = 'fortesting',
        )
        resp = self.client.get(reverse('catalog:authors'))
        self.assertEqual(str(resp.context['user']), 'test_user')
        self.assertEqual(resp.status_code, 200)


class TestAuthorListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for entire class. Runs once.
        WARNING: Don't use this if one of the test methods will change
        the data.
        """
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
        """Set up test data for each test in the class.
        Runs once for every test method in the class.
        """
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
        resp = self.client.get('/catalog/authors/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalog/authors.html')

    def test_pagination_is_ten(self):
        resp = self.client.get('/catalog/authors/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertEqual(
            len(resp.context['list_of_all_authors']), 10
            )

    def test_view_lists_all_authors(self):
        resp = self.client.get(reverse('catalog:authors') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertEqual(
            len(resp.context['list_of_all_authors']), 3
        )