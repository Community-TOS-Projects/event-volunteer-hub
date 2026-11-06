from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

LINK_TEXT = 'Log In / Sign Up'

class LoginSignupLinkTest(TestCase):
    """Tests for the Log In / Sign Up header link added for issue #21."""

    def test_link_shown_to_logged_out_user_on_public_pages(self):
        """Logged-out users see the link on every public page."""
        for name in ['accounts:homepage', 'accounts:login', 'accounts:signup']:
            response = self.client.get(reverse(name))
            self.assertContains(response, LINK_TEXT)

    def test_link_hidden_from_logged_in_user(self):
        """Logged-in users do not see the link."""
        user = get_user_model().objects.create_user(
            email='volunteer@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Volunteer',
            is_client=False,
        )
        self.client.force_login(user)
        response = self.client.get(reverse('accounts:homepage'))
        self.assertNotContains(response, LINK_TEXT)

    def test_link_routes_to_login_view(self):
        """The link points to the login page, which shows the login form."""
        response = self.client.get(reverse('accounts:homepage'))
        self.assertContains(response, f'href="{reverse("accounts:login")}"')

        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_page_links_to_signup(self):
        """The login page has a link to the sign-up page."""
        response = self.client.get(reverse('accounts:login'))
        self.assertContains(response, f'href="{reverse("accounts:signup")}"')

    def test_homepage_signup_buttons_still_work(self):
        """The existing homepage sign-up buttons still point to the sign-up page."""
        response = self.client.get(reverse('accounts:homepage'))
        self.assertContains(response, f'href="{reverse("accounts:signup")}"')