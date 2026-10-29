from django.contrib import admin

from meethub.events.models import Category, Event, Organization, Shift, Attendance

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'description')
    fields = ('name', 'description')


admin.site.register(Category, CategoryAdmin)


class EventAdmin(admin.ModelAdmin):

    list_display = ('name', 'venue', 'date', 'start_time', 'end_time')
    fields = ('category', 'name', 'creator', 'details', 'venue', 'date', ('start_time', 'end_time'))
    search_fields = ('name', 'details')

admin.site.register(Event, EventAdmin)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'website', 'contact_email', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'website', 'contact_email')
    list_filter = ('created_at', 'updated_at')


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'start_time', 'end_time', 'description', 'capacity')
    search_fields = ('name', 'event__name', 'description')
    list_filter = ('start_time', 'end_time')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'shift', 'status', 'hours_recorded')
    search_fields = ('userusername', 'event__name')
    list_filter = ('status', 'hours_recorded')
