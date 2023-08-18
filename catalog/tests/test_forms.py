import pytest

from datetime import timedelta

from django.test import TestCase
from catalog.forms import *


class TestRenewBookForm(TestCase):
    
    def test_form_label(self):
        form = RenewBookForm()
        self.assertTrue(
            form.fields['extend_days'].label in ['extend_days', None]
            # check field label in list because it could be None
        )

    def test_help_text(self):
        form = RenewBookForm()
        self.assertEqual(
            form.fields['extend_days'].help_text,
            'Select 3, 7, or 14 days for an extension from now.'
        )

    def test_valid_extension_days(self):
        for days in (3, 7, 14):
            form = RenewBookForm(data={'extend_days': timedelta(days=days)})
            # use the `data` argument with key-value pair to input form fields
            self.assertTrue(form.is_valid())

    def test_invalid_extension_days(self):
        invalid_days = set(i for i in range(1, 16)) - set([3, 7, 14])
        for days in invalid_days:
            form = RenewBookForm(data={'extend_days': timedelta(days=days)})
            self.assertFalse(form.is_valid())


class TestUserRegistrationForm(TestCase):

    def test_form_first_name_field_label_and_length(self):
        form = UserRegistrationForm()
        self.assertTrue(
            form.fields['first_name'].label in ['first_name', None]
        )
        self.assertEqual(
            form.fields['first_name'].max_length, 101
        )

    def test_form_first_name_field_label_and_length(self):
        form = UserRegistrationForm()
        self.assertTrue(
            form.fields['last_name'].label in ['last_name', None]
        )
        self.assertEqual(
            form.fields['last_name'].max_length, 101
        )

    def test_form_email_field_label(self):
        form = UserRegistrationForm()
        self.assertTrue(
            form.fields['email'].label in ['email', None]
        )