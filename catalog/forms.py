from datetime import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as gtl  # this is for future translation needs


class RenewBookForm(forms.Form):
    renewal_date = forms.DurationField(help_text='Enter 3, 7, or 14 days for an extension from now.')

    def clean_renewal_date(self):
        data = self.clean_data['renewal_date']

        if data not in [3, 7, 14]:
            raise ValidationError(gtl('Extension must be one of 3, 7 or 14 days.'))

        return data
