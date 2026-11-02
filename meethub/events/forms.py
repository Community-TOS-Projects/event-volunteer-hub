from django import forms

from meethub.events.models import Event, Category


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
        input_formats=['%m/%d/%Y', '%Y-%m-%d'],  # Ajusta según el formato de tu widget
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'datetimepicker1',
            'data-td-target': '#datetimepicker1'
        })
    )

    class Meta:
        model = Event
        fields = ('category', 'name', 'details', 'venue', 'start_time', 'end_time', 'date')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control'}),  
        }

