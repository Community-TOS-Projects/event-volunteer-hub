from django.db import migrations


def create_default_categories(apps, schema_editor):
    Category = apps.get_model('events', 'Category')

    categories = [
        {
            'name': 'Community Service',
            'description': 'Volunteer activities that support local communities.'
        },
        {
            'name': 'Volunteer Opportunity',
            'description': 'Events focused on volunteer recruitment and participation.'
        },
        {
            'name': 'Fundraiser',
            'description': 'Events intended to raise funds for organizations or causes.'
        },
        {
            'name': 'Community Event',
            'description': 'General community-focused gatherings and activities.'
        },
    ]

    for category in categories:
        Category.objects.get_or_create(
            name=category['name'],
            defaults={
                'description': category['description']
            }
        )


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_alter_category_id_alter_event_details_alter_event_id'),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]