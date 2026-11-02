from django.test import TestCase
from django.shortcuts import reverse
from django.urls import reverse

from meethub.accounts.models import Account
from meethub.events.models import Event, Category, User
from meethub.comments.models import Comment



class CommentDeleteViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='iyanu', password=12345, email='iyanu@gmail.com')
        self.attendee = User.objects.create_user(username='tobi', password=56789)
        self.attendee.save()
        self.user.save()
        self.category = Category.objects.create(name='Technology', description='This is the future')
        self.event = Event.objects.create(name='Party Outside', details='This party is gonna be banging again',
                                          venue='Mapo Hall',
                                          date='2018-05-18', time='12:25:00', category=self.category, creator=self.user)
        self.comment = Comment.objects.create(comment='Hey yo', event=self.event, created_by=self.user)


    def test_delete_comment_url_exists_at_desired_location(self):
        comment = Comment.objects.create(comment='Hey yo', event=self.event, created_by=self.user)
        self.client.login(username='iyanu', password=12345)
        response = self.client.get(reverse('comments:comment-delete', kwargs={'pk': self.comment.pk}))

        # Check the user is logged in
        # self.assertEqual(str(response.context['user']), 'iyanu')

        # Check that we got a response 'success'
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='iyanu', password='12345')
        response = self.client.get(reverse('comments:comment-delete', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='iyanu', password='12345')
        response = self.client.get(reverse('comments:comment-delete', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments/delete.html')

    def test_delete_view_redirect_to_event_detail_view(self):
        self.client.login(username='iyanu', password='12345')
        response = self.client.get(reverse('comments:comment-delete', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.event.get_absolute_url())


class CommentReplyViewTest(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(
            email='reply-author@example.com',
            password='reply-password',
            first_name='Reply',
            last_name='Author',
        )
        self.category = Category.objects.create(
            name='Technology',
            description='This is the future',
        )
        self.event = Event.objects.create(
            name='Community Meetup',
            details='A community event',
            venue='Mapo Hall',
            date='2026-05-18',
            time='12:25:00',
            category=self.category,
            creator=self.user,
        )
        self.comment = Comment.objects.create(
            comment='Looking forward to this event',
            event=self.event,
            created_by=self.user,
        )
        self.reply_url = reverse(
            'comments:comment-detail',
            kwargs={'comment_id': self.comment.pk, 'event_id': self.event.pk},
        )

    def test_signed_in_user_can_post_reply_and_is_redirected_to_event(self):
        self.client.login(email='reply-author@example.com', password='reply-password')

        response = self.client.post(self.reply_url, {'comment': 'I will be there'})

        self.assertRedirects(
            response,
            self.event.get_absolute_url(),
            fetch_redirect_response=False,
        )
        reply = Comment.objects.get(comment='I will be there')
        self.assertEqual(reply.event, self.event)
        self.assertEqual(reply.parent, self.comment)
        self.assertEqual(reply.created_by, self.user)

    def test_empty_reply_is_not_saved(self):
        self.client.login(email='reply-author@example.com', password='reply-password')
        initial_comment_count = Comment.objects.count()

        response = self.client.post(self.reply_url, {'comment': ''})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), initial_comment_count)

    def test_anonymous_user_cannot_post_reply(self):
        initial_comment_count = Comment.objects.count()

        response = self.client.post(self.reply_url, {'comment': 'Anonymous reply'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), initial_comment_count)

    def test_reply_page_loads_for_valid_event_and_comment(self):
        self.client.login(email='reply-author@example.com', password='reply-password')

        response = self.client.get(self.reply_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments/detail.html')
        self.assertEqual(response.context['comment'], self.comment)

    def test_reply_page_returns_404_for_invalid_event_id(self):
        self.client.login(email='reply-author@example.com', password='reply-password')
        url = reverse(
            'comments:comment-detail',
            kwargs={'comment_id': self.comment.pk, 'event_id': 99999},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_reply_page_returns_404_for_invalid_comment_id(self):
        self.client.login(email='reply-author@example.com', password='reply-password')
        url = reverse(
            'comments:comment-detail',
            kwargs={'comment_id': 99999, 'event_id': self.event.pk},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
