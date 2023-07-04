import pytest

from datetime import timedelta

from django.test import TestCase
from catalog.forms import *


class TestRenewBookForm(TestCase):
    
    def test_form_label(self):
        form = RenewBookForm()
        self.assertTrue(
            form.fields['extend_days'].label in ['extend_days', None]
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
            self.assertTrue(form.is_valid())

    def test_invalid_extension_days(self):
        invalid_days = set(i for i in range(1, 15)) - set([3, 7, 14])
        for days in invalid_days:
            form = RenewBookForm(data={'extend_days': timedelta(days=days)})
            self.assertFalse(form.is_valid())