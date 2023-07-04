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
        pass

    def test_invalid_extension_days(self):
        pass