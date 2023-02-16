from datetime import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as gtl  # this is for future translation needs


EXTENSION_DAYS = [3, 7, 14]

class RenewBookForm(forms.Form):
    extend_days = forms.DurationField(
        required=True,
        help_text='Enter 3, 7, or 14 days for an extension from now.',
        widget=forms.Select(days=EXTENSION_DAYS),
    )

    def clean_extend_days(self):
        data = self.clean_data['extend_days']

        if data not in [3, 7, 14]:
            raise ValidationError(gtl('Please select the amount of days to extend.'))

        return data
