import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='volunteer@example.com',
            password='OldPassword123!',
            first_name='Test',
            last_name='Volunteer',
        )

    def test_login_page_links_to_password_reset(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertContains(response, reverse('accounts:password_reset'))

    def test_password_reset_page_loads(self):
        response = self.client.get(reverse('accounts:password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_reset_email_sent_for_registered_email(self):
        response = self.client.post(reverse('accounts:password_reset'), {'email': 'volunteer@example.com'})
        self.assertRedirects(response, reverse('accounts:password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/accounts/reset/', mail.outbox[0].body)

    def test_unknown_email_gets_same_response_and_no_email(self):
        response = self.client.post(reverse('accounts:password_reset'), {'email': 'nobody@example.com'})
        self.assertRedirects(response, reverse('accounts:password_reset_done'))
        self.assertEqual(len(mail.outbox), 0)

    def test_full_reset_changes_password(self):
        self.client.post(reverse('accounts:password_reset'), {'email': 'volunteer@example.com'})
        link = re.search(r'http://testserver(\S+)', mail.outbox[0].body).group(1)

        # The link redirects to a "set-password" page, which is where the form is posted.
        response = self.client.get(link, follow=True)
        set_password_url = response.redirect_chain[-1][0]

        response = self.client.post(set_password_url, {
            'new_password1': 'NewPassword456!',
            'new_password2': 'NewPassword456!',
        })
        self.assertRedirects(response, reverse('accounts:password_reset_complete'))

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword456!'))