from datetime import date, time

import factory

from meethub.accounts.factories import AccountFactory
from meethub.events.models import Event, Category


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = 'Software'
    description = 'For software developers'


class EventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Event
 
    name = 'Pycon'
    details = 'For Python developers'
    venue = 'jand'
    date = factory.LazyFunction(date.today)
    start_time = time(9, 0)
    end_time = time(10, 0)
    category = factory.SubFactory(CategoryFactory)
    creator = factory.SubFactory(AccountFactory)
    num_of_attendees = 1

    @factory.post_generation
    def attendees(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for attendee in extracted:
                self.attendees.add(attendee)




