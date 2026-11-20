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
    class SignUpMode(models.TextChoices):
        DIRECT = 'direct', 'Direct'
        APPROVAL = 'approval', 'Approval required'

    name = models.CharField(max_length=50)
    details = tinymce_models.HTMLField()
    venue = models.CharField(max_length=200)
    date = models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    start_time = models.TimeField(help_text='Please use the following format: <em>HH:MM:SS<em>')
    end_time = models.TimeField(help_text='Please use the following format: <em>HH:MM:SS<em>')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    signup_mode = models.CharField(
        max_length=10,
        choices=SignUpMode.choices,
        default=SignUpMode.DIRECT,
    )
    attendees = models.ManyToManyField(Account, related_name='attending', blank=True)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['date', 'start_time', 'end_time']

    def clean(self):
        super().clean()
        if self.capacity is None:
            if self._state.adding:
                raise ValidationError({'capacity': 'Event capacity is required.'})
        elif self.capacity < 1:
            raise ValidationError({'capacity': 'Event capacity must be at least one.'})
        if (
            self.start_time is not None
            and self.end_time is not None
            and self.end_time <= self.start_time
        ):
            raise ValidationError({'end_time': 'Event end time must be later than its start time.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('events:event-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    def get_number_of_attendees(self):
        return self.attendees.all().count()

    def get_number_of_participants(self):
        attendee_ids = set(self.attendees.values_list('pk', flat=True))
        signup_ids = set(
            SignUp.objects.filter(
                event_id=self.pk,
                status__in=SignUp.ACTIVE_STATUSES,
            ).values_list('user_id', flat=True)
        )
        return len(attendee_ids | signup_ids)

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

    def clean(self):
        super().clean()
        if not self.event_id or not self.start_time or not self.end_time:
            return

        event = self.event
        current_timezone = timezone.get_current_timezone()
        # TODO: Revisit overnight shifts; this same-day Event window rejects work after midnight.
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
        if shift_start < shift_end:
            overlapping_shifts = Shift.objects.filter(
                event_id=self.event_id,
                start_time__lt=shift_end,
                end_time__gt=shift_start,
            )
            if self.pk:
                overlapping_shifts = overlapping_shifts.exclude(pk=self.pk)
            if overlapping_shifts.exists():
                errors['start_time'] = 'Shift must not overlap another shift for this event.'
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_number_of_volunteers(self):
        return SignUp.objects.filter(
            shift=self,
            status__in=SignUp.ACTIVE_STATUSES,
        ).values('user_id').distinct().count()


class SignUp(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        DECLINED = 'declined', 'Declined'
        CANCELLED = 'cancelled', 'Cancelled'

    ACTIVE_STATUSES = (StatusChoices.PENDING, StatusChoices.CONFIRMED)

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='signups')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='signups')
    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        related_name='signups',
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'shift'),
                condition=models.Q(
                    shift__isnull=False,
                    status__in=('pending', 'confirmed'),
                ),
                name='unique_active_signup_per_user_shift',
            ),
            models.UniqueConstraint(
                fields=('user', 'event'),
                condition=models.Q(
                    shift__isnull=True,
                    status__in=('pending', 'confirmed'),
                ),
                name='unique_active_reserve_signup_per_user_event',
            ),
        ]

    def clean(self):
        super().clean()
        errors = {}

        if self.shift_id and self.event_id and self.shift.event_id != self.event_id:
            errors['shift'] = 'The selected shift must belong to this event.'

        if self.status not in self.ACTIVE_STATUSES or not self.event_id or not self.user_id:
            if errors:
                raise ValidationError(errors)
            return

        event = self.event
        if event.capacity is None:
            errors['event'] = 'Sign-ups are unavailable until this event has a capacity.'
        else:
            participant_ids = set(event.attendees.values_list('pk', flat=True))
            participant_ids.update(
                SignUp.objects.filter(
                    event_id=event.pk,
                    status__in=self.ACTIVE_STATUSES,
                ).values_list('user_id', flat=True)
            )
            if self.user_id not in participant_ids and len(participant_ids) >= event.capacity:
                errors['event'] = 'This event has reached its participant capacity.'

        if self.shift_id:
            active_volunteer_ids = set(
                SignUp.objects.filter(
                    shift_id=self.shift_id,
                    status__in=self.ACTIVE_STATUSES,
                ).exclude(pk=self.pk).values_list('user_id', flat=True)
            )
            if self.user_id not in active_volunteer_ids and len(active_volunteer_ids) >= self.shift.capacity:
                errors['shift'] = 'This shift has reached its volunteer capacity.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        shift_name = self.shift.name if self.shift_id else 'Event reserve'
        return f'{self.user} - {self.event} - {shift_name} - {self.get_status_display()}'
    
#ATTENDANCE MODEL
class Attendance(models.Model):
    class StatusChoices(models.TextChoices):
        ATTENDED = 'attended', 'Attended'
        ABSENT = 'absent', 'Absent'

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='attendances')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='attendances', null=True, blank=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    hours_recorded = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.shift_id and self.event_id and self.shift.event_id != self.event_id:
            raise ValidationError({'shift': 'The attendance shift must belong to the same event.'})

    class Meta:
        unique_together = ('user', 'shift')

    def __str__(self):
        return f"{self.user} - {self.shift.start_time.strftime('%Y-%m-%d %H:%M') if self.shift else 'No Shift'} - {self.get_status_display()}"
