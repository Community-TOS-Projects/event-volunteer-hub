# Regression tests for the event attendance workflow (attend / not attend).
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from meethub.accounts.models import Account
from meethub.events.models import Category, Event


class AttendanceTestBase(TestCase):
    # Shared setup used by the test classes below

    def setUp(self):
        # Create two accounts
        self.account = Account.objects.create_user(
            email='volunteer@example.com', password='testpass123',
            first_name='Vera', last_name='Volunteer', is_client=False)
        self.other_account = Account.objects.create_user(
            email='other@example.com', password='testpass123',
            first_name='Otto', last_name='Other', is_client=False)

        # Create a category and an event
        self.category = Category.objects.create(
            name='Technology', description='This is the future')
        self.event = Event.objects.create(
            name='Party Outside', details='This party is gonna be banging again',
            venue='Mapo Hall', date='2018-05-18', time='12:25:00',
            category=self.category, creator=self.account)

        # Build the URLs used in the tests
        self.attend_url = reverse(
            'events:attend_event', kwargs={'event_id': self.event.pk})
        self.not_attend_url = reverse(
            'events:not_attend_event', kwargs={'event_id': self.event.pk})
        self.detail_url = reverse(
            'events:event-detail', kwargs={'pk': self.event.pk})

    def is_attending(self, account):
        # Check if the account is in the event's attendee list
        return self.event.attendees.filter(pk=account.pk).exists()


class AttendEventViewTest(AttendanceTestBase):

    def test_setup_uses_configured_custom_account_model(self):
        # Confirm the tests use the custom Account model
        self.assertEqual(settings.AUTH_USER_MODEL, 'accounts.Account')
        self.assertIs(get_user_model(), Account)
        self.assertIsInstance(self.account, Account)

    def test_authenticated_account_can_attend_event(self):
        # Log in, attend, and check the account was added
        self.client.force_login(self.account)
        self.assertFalse(self.is_attending(self.account))
        self.client.post(self.attend_url)
        self.assertTrue(self.is_attending(self.account))
        self.assertEqual(self.event.get_number_of_attendees(), 1)

    def test_attend_redirects_to_event_detail(self):
        # Check the redirect back to the event page
        self.client.force_login(self.account)
        response = self.client.post(self.attend_url)
        self.assertRedirects(
            response, self.detail_url, fetch_redirect_response=False)

    def test_attending_twice_keeps_a_single_attendance(self):
        # Attend twice and check there is only one attendance
        self.client.force_login(self.account)
        self.client.post(self.attend_url)
        self.client.post(self.attend_url)
        self.assertEqual(self.event.get_number_of_attendees(), 1)

    def test_attending_does_not_affect_other_attendees(self):
        # Check an existing attendee is kept when someone else attends
        self.event.attendees.add(self.other_account)
        self.client.force_login(self.account)
        self.client.post(self.attend_url)
        self.assertTrue(self.is_attending(self.account))
        self.assertTrue(self.is_attending(self.other_account))

    def test_anonymous_user_cannot_attend_event(self):
        # Logged-out user is redirected to login and not added
        response = self.client.post(self.attend_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        self.assertEqual(self.event.get_number_of_attendees(), 0)

    def test_attend_nonexistent_event_returns_404(self):
        # Attending an event that does not exist gives a 404
        self.client.force_login(self.account)
        url = reverse('events:attend_event', kwargs={'event_id': 999999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)


class NotAttendEventViewTest(AttendanceTestBase):

    def test_attending_account_can_leave_event(self):
        # Start as an attendee, leave, and check the account was removed
        self.event.attendees.add(self.account)
        self.client.force_login(self.account)
        self.client.post(self.not_attend_url)
        self.assertFalse(self.is_attending(self.account))
        self.assertEqual(self.event.get_number_of_attendees(), 0)

    def test_leave_redirects_to_event_detail(self):
        # Check the redirect back to the event page
        self.event.attendees.add(self.account)
        self.client.force_login(self.account)
        response = self.client.post(self.not_attend_url)
        self.assertRedirects(
            response, self.detail_url, fetch_redirect_response=False)

    def test_leaving_does_not_affect_other_attendees(self):
        # Check other attendees are kept when one account leaves
        self.event.attendees.add(self.account, self.other_account)
        self.client.force_login(self.account)
        self.client.post(self.not_attend_url)
        self.assertFalse(self.is_attending(self.account))
        self.assertTrue(self.is_attending(self.other_account))

    def test_leaving_when_not_attending_changes_nothing(self):
        # Leaving without attending causes no error and no change
        self.event.attendees.add(self.other_account)
        self.client.force_login(self.account)
        response = self.client.post(self.not_attend_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.is_attending(self.account))
        self.assertTrue(self.is_attending(self.other_account))

    def test_anonymous_user_cannot_leave_event(self):
        # Logged-out user is redirected to login and nobody is removed
        self.event.attendees.add(self.account)
        response = self.client.post(self.not_attend_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        self.assertTrue(self.is_attending(self.account))

    def test_leave_nonexistent_event_returns_404(self):
        # Leaving an event that does not exist gives a 404
        self.client.force_login(self.account)
        url = reverse('events:not_attend_event', kwargs={'event_id': 999999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_attend_then_leave_round_trip(self):
        # Attend, then leave, and check the state after each step
        self.client.force_login(self.account)
        self.client.post(self.attend_url)
        self.assertTrue(self.is_attending(self.account))
        self.client.post(self.not_attend_url)
        self.assertFalse(self.is_attending(self.account))