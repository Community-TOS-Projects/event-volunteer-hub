from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LogoutViewTest(TestCase):
    """Tests for the logout option added for issue #9."""

    def setUp(self):
        # Create a regular (non-admin) user and log them in before each test
        self.user = get_user_model().objects.create_user(
            email='volunteer@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Volunteer',
            is_client=False,
        )
        self.client.force_login(self.user)

    def test_logout_button_shown_to_logged_in_user(self):
        """A logged-in user sees the logout form in the navigation dropdown."""
        response = self.client.get(reverse('events:event-list'))

        # Check the form posts to the logout URL and includes a CSRF token
        self.assertContains(response, f'action="{reverse("accounts:logout")}"')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_logout_post_ends_session_and_shows_logged_out_page(self):
        """Logging out with POST ends the session and shows the logged-out page."""
        response = self.client.post(reverse('accounts:logout'))

        # Check our confirmation page is shown instead of Grappelli's
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/logged_out.html')

        # Check the user is no longer stored in the session
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logged_out_page_links_to_login_and_signup(self):
        """The logged-out page links back to the login and signup pages."""
        response = self.client.post(reverse('accounts:logout'))
        self.assertContains(response, reverse('accounts:login'))
        self.assertContains(response, reverse('accounts:signup'))

    def test_protected_page_requires_login_after_logout(self):
        """After logout, protected pages redirect to the login page."""
        self.client.post(reverse('accounts:logout'))
        response = self.client.get(reverse('events:event-list'))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('events:event-list')}",
        )

    def test_logout_get_not_allowed(self):
        """Logout through a plain link (GET) is rejected, as Django 5 requires."""
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 405)
