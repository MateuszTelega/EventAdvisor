import re
from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.core.exceptions import ValidationError
from .models import Event


def capitalized_validator(value: str):
    if value[0].islower():
        raise ValidationError('Value must be capitalized!')


class FutureDateField(forms.DateField):
    def validate(self, value):
        super().validate(value)
        if value < date.today():
            raise ValidationError('Only future dates allowed here.')


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'

    title = forms.CharField(validators=[capitalized_validator])
    date_from = FutureDateField(
        initial=date.today,
        widget=forms.DateInput(format='%d-%m-%Y'),
        input_formats=('%d-%m-%Y', )
    )
    date_to = FutureDateField(
        initial=date.today,
        widget=forms.DateInput(format='%d-%m-%Y'),
        input_formats=('%d-%m-%Y', )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            Row(Column('date_from'), Column('start_time'), Column('date_to'), Column('end_time')),
            'place',
            'picture',
            'description',
            'event_type',
            'users',
            Submit('submit', 'Submit'),
        )

    def clean_description(self):
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        cleaned = '. '.join(sentence.capitalize() for sentence in sentences)
        return cleaned
