from datetime import datetime

from django.test import TestCase

from meethub.accounts.models import Account
from meethub.events.models import Attendance, Event, Category, Organization, Shift


class EventModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.account = Account.objects.create_user(
            email='iyanu@gmail.com',
            password='secret123',
            first_name='Iyanu',
            last_name='Ajao',
        )
        cls.category = Category.objects.create(name='Technology', description='This is the future')
        cls.event = Event.objects.create(
            name='Party Outside',
            details='This party is gonna be banging again',
            venue='Mapo Hall',
            date='2018-05-18',
            time='12:25:00',
            category=cls.category,
            creator=cls.account,
        )

    def test_name_label(self):
        field_label = self.event._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_details_label(self):
        field_label = self.event._meta.get_field('details').verbose_name
        self.assertEqual(field_label, 'details')

    def test_venue_label(self):
        field_label = self.event._meta.get_field('venue').verbose_name
        self.assertEqual(field_label, 'venue')

    def test_date_label(self):
        field_label = self.event._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'date')

    def test_time_label(self):
        field_label = self.event._meta.get_field('time').verbose_name
        self.assertEqual(field_label, 'time')

    def test_name_max_length(self):
        max_length = self.event._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_venue_max_length(self):
        max_length = self.event._meta.get_field('venue').max_length
        self.assertEqual(max_length, 200)

    def test_event_object_name(self):
        self.assertEqual(str(self.event), 'Party Outside')

    def test_get_absolute_url(self):
        self.assertTrue(self.event.get_absolute_url().startswith('/events/'))

    def test_get_absolute_url_not_none(self):
        self.assertIsNotNone(self.event.get_absolute_url())

    def test_get_number_of_attendees(self):
        self.assertEqual(self.event.get_number_of_attendees(), 0)

    def test_get_comments_number(self):
        self.assertEqual(self.event.get_comments_number(), 0)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Event._meta.verbose_name_plural), 'events')


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Technology', description='This is the future')

    def test_category_object_name(self):
        self.assertEqual(str(self.category), 'Technology')

    def test_category_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), 'categories')


class OrganizationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.organization = Organization.objects.create(
            name='Tech Corp',
            description='A technology company',
            website='https://www.techcorp.com',
            contact_email='contact@techcorp.com',
        )

    def test_organization_object_name(self):
        self.assertEqual(str(self.organization), 'Tech Corp')

    def test_organization_verbose_name_plural(self):
        self.assertEqual(str(Organization._meta.verbose_name_plural), 'organizations')

    def test_organization_fields(self):
        self.assertEqual(self.organization.description, 'A technology company')
        self.assertEqual(self.organization.website, 'https://www.techcorp.com')
        self.assertEqual(self.organization.contact_email, 'contact@techcorp.com')

    def test_organization_timestamps(self):
        self.assertIsNotNone(self.organization.created_at)
        self.assertIsNotNone(self.organization.updated_at)


class AttendanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(
            email='iyanu@example.com',
            password='secret123',
            first_name='Iyanu',
            last_name='Ajao',
        )
        cls.category = Category.objects.create(name='Technology', description='This is the future')
        cls.event = Event.objects.create(
            name='Tech Conference',
            details='A conference for tech enthusiasts',
            venue='Convention Center',
            date='2023-06-01',
            time='09:00:00',
            category=cls.category,
            creator=cls.user,
        )
        cls.shift = Shift.objects.create(
            event=cls.event,
            start_time=datetime(2023, 6, 1, 9, 0, 0),
            end_time=datetime(2023, 6, 1, 17, 0, 0),
            description='Morning shift',
            max_volunteers=5,
        )
        cls.attendance = Attendance.objects.create(
            user=cls.user,
            event=cls.event,
            shift=cls.shift,
            status='pending',
            hours_recorded=8,
        )

    def test_attendance_object_name(self):
        expected_object_name = (
            f"{self.user} - {self.shift.start_time.strftime('%Y-%m-%d %H:%M')} - {self.attendance.get_status_display()}"
        )
        self.assertEqual(str(self.attendance), expected_object_name)

    def test_attendance_verbose_name_plural(self):
        self.assertEqual(str(Attendance._meta.verbose_name_plural), 'attendances')

    def test_timestamps(self):
        self.assertIsNotNone(self.attendance.created_at)
        self.assertIsNotNone(self.attendance.updated_at)

    def test_status_choices(self):
        for status_value, _ in Attendance.StatusChoices.choices:
            shift = Shift.objects.create(
                event=self.event,
                start_time=datetime(2023, 6, 1, 9, 0, 0),
                end_time=datetime(2023, 6, 1, 17, 0, 0),
                description=f'{status_value} shift',
                max_volunteers=5,
            )
            attendance = Attendance.objects.create(
                user=self.user,
                event=self.event,
                shift=shift,
                status=status_value,
                hours_recorded=5,
            )
            self.assertIn(attendance.status, [choice[0] for choice in Attendance.StatusChoices.choices])

        self.assertEqual(len([choice[0] for choice in Attendance.StatusChoices.choices]), 4)
