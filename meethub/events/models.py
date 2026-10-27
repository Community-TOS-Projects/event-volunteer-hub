from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User

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
    time = models.TimeField(help_text='Please use the following format: <em>HH:MM:SS<em>')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Account, related_name='attending', blank=True)
    num_of_attendees = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['date', 'time']

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
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='shifts')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(max_length=500, default='')
    max_volunteers = models.PositiveIntegerField(default=1)
    volunteers = models.ManyToManyField(Account, related_name='shifts', blank=True)

    def __str__(self):
        return f"{self.event.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')}"

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
