from django.test import TestCase
from django.contrib.auth import get_user_model
from meethub.events.forms import EventForm
from meethub.events.models import Event, Category

User = get_user_model()


class EventFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Technology', description='This is the future')
        self.user = User.objects.create_user(
            email='iyanu@gmail.com',
            password='12345',
            first_name='Iyanu',
            last_name='User',
            is_client=False,
        )
        Event.objects.create(
            name='Party Outside',
            details='This party is gonna be banging again',
            venue='Mapo Hall',
            date='2018-05-18',
            start_time='12:25:00',
            end_time='13:25:00',
            category=self.category,
            creator=self.user,
        )

    def test_event_form_invalid(self):
        form = EventForm(data={
            'name': '',
            'details': '',
            'venue': 'Mapo Hall',
            'date': '2018-05-18',
            'start_time': '12:25:00',
            'end_time': '13:25:00',
            'category': 'category',
        })
        self.assertFalse(form.is_valid())

    def test_event_form_date_field_label(self):
        form = EventForm()
        self.assertTrue(form.fields['date'].label is None or form.fields['date'].label == 'Date')

    def test_event_form_date_field_help_text(self):
        form = EventForm()
        self.assertEqual(form.fields['date'].help_text, 'Please use the following format: <em>YYYY-MM-DD</em>.')

    def test_event_form_start_time_field_label(self):
        form = EventForm()
        self.assertTrue(form.fields['start_time'].label is None or form.fields['start_time'].label == 'Start time')
 
    def test_event_form_start_time_field_help_text(self):
        form = EventForm()
        self.assertEqual(form.fields['start_time'].help_text, 'Please use the following format: <em>HH:MM:SS<em>')

    def test_event_form_end_time_field_label(self):
        form = EventForm()
        self.assertTrue(form.fields['end_time'].label is None or form.fields['end_time'].label == 'End time')

    def test_event_form_end_time_field_help_text(self):
        form = EventForm()
        self.assertEqual(form.fields['end_time'].help_text, 'Please use the following format: <em>HH:MM:SS<em>')

    def test_event_form_name_field_label(self):
        form = EventForm()
        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'Name')

    def test_event_form_details_field_label(self):
        form = EventForm()
        self.assertTrue(form.fields['details'].label is None or form.fields['details'].label == 'Details')

    def test_event_form_venue_field_label(self):
        form = EventForm()
        self.assertTrue(form.fields['venue'].label is None or form.fields['venue'].label == 'Venue')

    def test_event_form_category_field_label(self):
        form = EventForm()
        self.assertTrue(form.fields['category'].label is None or form.fields['category'].label == 'Category')




















