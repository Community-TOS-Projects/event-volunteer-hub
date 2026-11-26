from django import forms
from django.forms import ValidationError
from django.utils.html import strip_tags

from meethub.events.models import Event, Category

import html

DETAILS_MAX_LENGTH = 1000

class EventForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    start_time = forms.TimeField(
        help_text='Please use the following format: <em>HH:MM:SS<em>',
        input_formats=['%I:%M %p', '%H:%M', '%H:%M:%S'],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'datetimepicker2',
            'data-td-target': '#datetimepicker2'
        })
    )
    end_time = forms.TimeField(
        help_text='Please use the following format: <em>HH:MM:SS<em>',
        input_formats=['%I:%M %p', '%H:%M', '%H:%M:%S'],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'datetimepicker3',
            'data-td-target': '#datetimepicker3'
        })
    )
 
    date = forms.DateField(
        help_text='Please use the following format: <em>YYYY-MM-DD</em>.',
        input_formats=['%m/%d/%Y', '%Y-%m-%d'],  
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'datetimepicker1',
            'data-td-target': '#datetimepicker1'
        })
    )

    def clean_details(self):
        details = self.cleaned_data['details']
        plain_text = html.unescape(strip_tags(details))
        plain_text = plain_text.replace('\r\n', '\n').strip()

        if len(plain_text) > DETAILS_MAX_LENGTH:
            raise ValidationError(
                f'Event details cannot exceed {DETAILS_MAX_LENGTH} characters. '
                f'You entered {len(plain_text)} characters.'
            )
        return details
        
    class Meta:
        model = Event
        fields = ('category', 'name', 'details', 'venue', 'start_time', 'end_time', 'date')
        help_texts = {
            'details': f'Maximum {DETAILS_MAX_LENGTH} characters.'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': DETAILS_MAX_LENGTH,
            }),
        }

