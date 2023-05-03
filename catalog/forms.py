from datetime import datetime, timedelta

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as gtl  # this is for future translation needs


EXTENSION_DAYS = [(timedelta(days=days), f"{days} days from now") for days in (3, 7, 14)]
class RenewBookForm(forms.Form):
    extend_days = forms.DurationField(
        required=True,
        help_text=gtl('Select 3, 7, or 14 days for an extension from now.'),
        widget=forms.Select(choices=EXTENSION_DAYS),
    )

    def clean_extend_days(self):
        # Note: the "clean" here is talking about both cleaning for malicious code and validating.

        data = self.cleaned_data['extend_days'] 
        # The use of "cleaned" instead of "clean" in code `self.cleaned_data`
        # is because the data has already been cleaned for malicious inputs once already.

        if data not in [tup[0] for tup in EXTENSION_DAYS]:
            raise ValidationError(gtl('Please select the amount of days to extend.'))

        return data