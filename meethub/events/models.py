from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import reverse
from django.utils import timezone

from tinymce import models as tinymce_models 

from meethub.accounts.models import Account


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50)
    details = tinymce_models.HTMLField()
    venue = models.CharField(max_length=200)
    date = models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    start_time = models.TimeField(help_text='Please use the following format: <em>HH:MM:SS<em>')
    end_time = models.TimeField(help_text='Please use the following format: <em>HH:MM:SS<em>')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Account, related_name='attending', blank=True)
    num_of_attendees = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['date', 'start_time', 'end_time']

    def get_absolute_url(self):
        return reverse('events:event-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    def get_number_of_attendees(self):
        return self.attendees.all().count()

    def get_comments_number(self):
        return self.comments.all().count()

#ORGANIZATION MODEL
class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=500, default='')
    website = models.URLField(max_length=200, blank=True)
    contact_email = models.EmailField(max_length=254, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
#SHIFT MODEL
class Shift(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='shifts')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(max_length=500, default='')
    capacity = models.PositiveIntegerField(default=1)
    volunteers = models.ManyToManyField(Account, related_name='shifts', blank=True)

    def clean(self):
        super().clean()
        if not self.event_id or not self.start_time or not self.end_time:
            return

        event = self.event
        current_timezone = timezone.get_current_timezone()
        event_start = datetime.combine(event.date, event.start_time)
        event_end = datetime.combine(event.date, event.end_time)
        shift_start = self.start_time
        shift_end = self.end_time

        if settings.USE_TZ:
            event_start = timezone.make_aware(event_start, current_timezone)
            event_end = timezone.make_aware(event_end, current_timezone)
            if timezone.is_naive(shift_start):
                shift_start = timezone.make_aware(shift_start, current_timezone)
            else:
                shift_start = shift_start.astimezone(current_timezone)
            if timezone.is_naive(shift_end):
                shift_end = timezone.make_aware(shift_end, current_timezone)
            else:
                shift_end = shift_end.astimezone(current_timezone)
        else:
            if timezone.is_aware(shift_start):
                shift_start = timezone.make_naive(shift_start, current_timezone)
            if timezone.is_aware(shift_end):
                shift_end = timezone.make_naive(shift_end, current_timezone)

        errors = {}
        if shift_start >= shift_end:
            errors['end_time'] = 'Shift end time must be after its start time.'
        if not event_start <= shift_start <= event_end:
            errors['start_time'] = 'Shift start time must fall within the event time range.'
        if not event_start <= shift_end <= event_end:
            errors['end_time'] = 'Shift end time must fall within the event time range.'
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_number_of_volunteers(self):
        return self.volunteers.all().count()
    
#ATTENDANCE MODEL
class Attendance(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        ATTENDED = 'attended', 'Attended'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='attendances')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='attendances', null=True, blank=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    hours_recorded = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'shift')

    def __str__(self):
        return f"{self.user} - {self.shift.start_time.strftime('%Y-%m-%d %H:%M') if self.shift else 'No Shift'} - {self.get_status_display()}"
