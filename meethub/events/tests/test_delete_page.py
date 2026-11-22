import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import formats

from meethub.events.models import Category, Event
from meethub.accounts.models import Account

class EventDeletePageTest(TestCase):
    """The delete confirmation page loads and shows the event's details."""

    def setUp(self):

        #Create the event's creator and log in as them
        self.account = Account.objects.create_user(
            email='creator@example.com', password="00000",
            first_name="test", last_name="Creator", is_client=False
        )
        self.client.force_login(self.account)

        #Create a category and an event

        self.category = Category.objects.create(name = "Community", description = "Community service events")
        self.event = Event.objects.create(name = "Park Cleanup", venue = "Central Park", date=datetime.date(2027,1,1), time=datetime.time(8, 30), category = self.category, creator =self.account)

        self.delete_url = reverse('events:event-delete', kwargs={'pk':self.event.pk})

    def test_delete_page_loads(self):
        """Opening the delete page returns 200 instead of a server error."""
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)

    def test_delete_page_uses_delete_template(self):
        """The delete page is rendered with events/delete.html"""
        response = self.client.get(self.delete_url)
        self.assertTemplateUsed(response, 'events/delete.html')

    def test_delete_page_shows_event_details(self):
        """The page shows the event's name, date, time, and venue."""
        response = self.client.get(self.delete_url)
        # Date and time are checked in the format that the template displays them in
        self.assertContains(response,"Park Cleanup")
        self.assertContains(response, formats.date_format(self.event.date, "DATE_FORMAT"))
        self.assertContains(response, formats.time_format(self.event.time, "TIME_FORMAT"))
        self.assertContains(response,"Central Park")

    
