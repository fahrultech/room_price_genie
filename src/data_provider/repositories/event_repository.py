from django.utils import timezone
from abc import ABC, abstractmethod
from data_provider.models import Event
from data_provider.utils import translate_event_filters

class IEventRepository(ABC):
    @abstractmethod
    def get_events(self, filters: dict):
        pass

    @abstractmethod
    def save_event(self, event_data: dict):
        pass

class EventRepository(IEventRepository):
    def get_events(self, filters: dict):
        translated_filters = translate_event_filters(filters)
        return Event.objects.filter(**translated_filters)

    def save_event(self, event_data: dict):
        event_data['timestamp'] = timezone.now()
        event = Event(**event_data)
        event.save()
        return event
